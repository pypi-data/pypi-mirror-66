#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only API for Things 3."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.3.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sqlite3
import sys
from random import shuffle
from os import environ
import getpass


# pylint: disable=R0904
class Things3():
    """Simple read-only API for Things 3."""
    # Variables
    debug = False
    database = None
    json = False
    tag_waiting = "Waiting" if not environ.get('TAG_WAITING') \
        else environ.get('TAG_WAITING')
    tag_mit = "MIT" if not environ.get('TAG_MIT') \
        else environ.get('TAG_MIT')
    tag_cleanup = "Cleanup" if not environ.get('TAG_CLEANUP') \
        else environ.get('TAG_CLEANUP')
    anonymize = bool(environ.get('ANONYMIZE'))

    # Database info
    FILE_DB = '/Library/Containers/'\
              'com.culturedcode.ThingsMac/Data/Library/'\
              'Application Support/Cultured Code/Things/Things.sqlite3'
    FILE_SQLITE = '/Users/' + getpass.getuser() + FILE_DB \
        if not environ.get('THINGSDB') else environ.get('THINGSDB')

    TABLE_TASK = "TMTask"
    TABLE_AREA = "TMArea"
    TABLE_TAG = "TMTag"
    TABLE_TASKTAG = "TMTaskTag"
    DATE_CREATE = "creationDate"
    DATE_MOD = "userModificationDate"
    DATE_DUE = "dueDate"
    DATE_START = "startDate"
    DATE_STOP = "stopDate"
    IS_INBOX = "start = 0"
    IS_ANYTIME = "start = 1"
    IS_SOMEDAY = "start = 2"
    IS_SCHEDULED = f"{DATE_START} IS NOT NULL"
    IS_NOT_SCHEDULED = f"{DATE_START} IS NULL"
    IS_DUE = f"{DATE_DUE} IS NOT NULL"
    IS_NOT_DUE = f"{DATE_DUE} IS NULL"
    IS_RECURRING = "recurrenceRule IS NOT NULL"
    IS_NOT_RECURRING = "recurrenceRule IS NULL"
    IS_TASK = "type = 0"
    IS_PROJECT = "type = 1"
    IS_HEADING = "type = 2"
    IS_TRASHED = "trashed = 1"
    IS_NOT_TRASHED = "trashed = 0"
    IS_OPEN = "status = 0"
    IS_CANCELLED = "status = 2"
    IS_DONE = "status = 3"

    # Query Index
    I_UUID = 0
    I_TITLE = 1
    I_CONTEXT = 2
    I_CONTEXT_UUID = 3
    I_DUE = 4
    I_CREATE = 5
    I_MOD = 6
    I_START = 7
    I_STOP = 8

    def __init__(self,
                 database=FILE_SQLITE,
                 tag_waiting='Waiting',
                 tag_mit='MIT',
                 json=False):
        self.database = database if database is not None else self.FILE_SQLITE
        self.tag_mit = tag_mit
        self.tag_waiting = tag_waiting
        self.json = json

    @staticmethod
    def anonymize_string(string):
        """Scramble text."""
        string = list(string)
        shuffle(string)
        string = ''.join(string)
        return string

    def anonymize_tasks(self, tasks):
        """Scramble output for screenshots."""
        result = tasks
        if self.anonymize:
            result = []
            for task in tasks:
                task = list(task)
                task[self.I_TITLE] = \
                    self.anonymize_string(str(task[self.I_TITLE]))
                task[self.I_CONTEXT] = \
                    self.anonymize_string(str(task[self.I_CONTEXT]))
                result.append(task)
        return result

    def get_inbox(self):
        """Get all tasks from the inbox."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_INBOX}
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_today(self):
        """Get all tasks from the today list."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_ANYTIME} AND
                TASK.{self.IS_SCHEDULED} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_someday(self):
        """Get someday tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_SOMEDAY} AND
                TASK.{self.IS_NOT_SCHEDULED} AND
                TASK.{self.IS_NOT_RECURRING} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_ANYTIME} AND
                            PROJECT.{self.IS_NOT_SCHEDULED} AND
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_ANYTIME} AND
                            HEADPROJ.{self.IS_NOT_SCHEDULED} AND
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC, TASK.creationdate DESC
                """
        return self.get_rows(query)

    def get_upcoming(self):
        """Get upcoming tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_SOMEDAY} AND
                TASK.{self.IS_SCHEDULED} AND
                TASK.{self.IS_NOT_RECURRING} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.startdate, TASK.todayIndex
                """
        return self.get_rows(query)

    def get_waiting(self):
        """Get waiting tasks."""
        return self.get_tag(self.tag_waiting)

    def get_mit(self):
        """Get most important tasks."""
        return self.get_tag(self.tag_mit)

    def get_tag(self, tag):
        """Get task with specific tag"""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TAGS.tags=(SELECT uuid FROM {self.TABLE_TAG}
                             WHERE title='{tag}'
                          )
                AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_anytime(self):
        """Get anytime tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_ANYTIME} AND
                TASK.{self.IS_NOT_SCHEDULED} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_ANYTIME} AND
                            PROJECT.{self.IS_NOT_SCHEDULED} AND
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_ANYTIME} AND
                            HEADPROJ.{self.IS_NOT_SCHEDULED} AND
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_completed(self):
        """Get completed tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_DONE}
                ORDER BY TASK.{self.DATE_STOP}
                """
        return self.get_rows(query)

    def get_cancelled(self):
        """Get cancelled tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_CANCELLED}
                ORDER BY TASK.{self.DATE_STOP}
                """
        return self.get_rows(query)

    def get_trashed(self):
        """Get trashed tasks."""
        query = f"""
                TASK.{self.IS_TRASHED} AND
                TASK.{self.IS_TASK}
                ORDER BY TASK.{self.DATE_STOP}
                """
        return self.get_rows(query)

    def get_all(self):
        """Get all tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                """
        return self.get_rows(query)

    def get_due(self):
        """Get due tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_DUE} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.{self.DATE_DUE}
                """
        return self.get_rows(query)

    def get_lint(self):
        """Get tasks that float around"""
        query = f"""
            TASK.{self.IS_NOT_TRASHED} AND
            TASK.{self.IS_OPEN} AND
            TASK.{self.IS_TASK} AND
            (TASK.{self.IS_SOMEDAY} OR TASK.{self.IS_ANYTIME}) AND
            TASK.project IS NULL AND
            TASK.area IS NULL AND
            TASK.actionGroup IS NULL
            """
        return self.get_rows(query)

    def get_empty_projects(self):
        """Get projects that are empty"""
        query = f"""
            TASK.{self.IS_NOT_TRASHED} AND
            TASK.{self.IS_OPEN} AND
            TASK.{self.IS_PROJECT}
            GROUP BY TASK.uuid
            HAVING
                (SELECT COUNT(uuid)
                 FROM TMTask
                 WHERE
                   project = TASK.uuid AND
                   {self.IS_NOT_TRASHED} AND
                   {self.IS_OPEN}
                ) = 0
            """
        return self.get_rows(query)

    def get_cleanup(self):
        """Tasks and projects that need work."""
        result = []
        result.extend(self.get_lint())
        result.extend(self.get_empty_projects())
        result.extend(self.get_tag(self.tag_cleanup))
        return result

    @staticmethod
    def get_not_implemented():
        """Not implemented warning."""
        return [["0", "not implemented", "no context", "0", "0", "0", "0",
                 "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]

    def get_rows(self, sql):
        """Query Things database."""

        sql = """
            SELECT DISTINCT
                TASK.uuid,
                TASK.title,
                CASE
                    WHEN AREA.title IS NOT NULL THEN AREA.title
                    WHEN PROJECT.title IS NOT NULL THEN PROJECT.title
                    WHEN HEADING.title IS NOT NULL THEN HEADING.title
                END,
                CASE
                    WHEN AREA.uuid IS NOT NULL THEN AREA.uuid
                    WHEN PROJECT.uuid IS NOT NULL THEN PROJECT.uuid
                END,
                CASE
                    WHEN TASK.recurrenceRule IS NULL
                    THEN date(TASK.dueDate,"unixepoch")
                ELSE NULL
                END,
                date(TASK.creationDate,"unixepoch"),
                date(TASK.userModificationDate,"unixepoch"),
                date(TASK.startDate,"unixepoch"),
                date(TASK.stopDate,"unixepoch")
            FROM
                TMTask AS TASK
            LEFT OUTER JOIN
                TMTask PROJECT ON TASK.project = PROJECT.uuid
            LEFT OUTER JOIN
                TMArea AREA ON TASK.area = AREA.uuid
            LEFT OUTER JOIN
                TMTask HEADING ON TASK.actionGroup = HEADING.uuid
            LEFT OUTER JOIN
                TMTask HEADPROJ ON HEADING.project = HEADPROJ.uuid
            LEFT OUTER JOIN
                TMTaskTag TAGS ON TASK.uuid = TAGS.tasks
            LEFT OUTER JOIN
                TMTag TAG ON TAGS.tags = TAG.uuid
            WHERE
                """ + sql

        if self.debug is True:
            print(sql)

        try:
            cursor = sqlite3.connect(self.database).cursor()
            cursor.execute(sql)
            tasks = cursor.fetchall()
            tasks = self.anonymize_tasks(tasks)
            if self.debug:
                for task in tasks:
                    print(task)
            return tasks
        except sqlite3.OperationalError as error:
            print(f"Could not query the database at: {self.database}.")
            print(f"Details: {error}.")
            sys.exit(2)

    def convert_task_to_model(self, task):
        """Convert task to model."""
        model = {'uuid': task[self.I_UUID],
                 'title': task[self.I_TITLE],
                 'context': task[self.I_CONTEXT],
                 'context_uuid': task[self.I_CONTEXT_UUID],
                 'due': task[self.I_DUE],
                 'created': task[self.I_CREATE],
                 'modified': task[self.I_MOD],
                 'started': task[self.I_START],
                 'stopped': task[self.I_STOP]
                 }
        return model

    def convert_tasks_to_model(self, tasks):
        """Convert tasks to model."""
        model = []
        for task in tasks:
            model.append(self.convert_task_to_model(task))
        return model

    functions = {
        "inbox": get_inbox,
        "today": get_today,
        "next": get_anytime,
        "backlog": get_someday,
        "upcoming": get_upcoming,
        "waiting": get_waiting,
        "mit": get_mit,
        "completed": get_completed,
        "cancelled": get_cancelled,
        "trashed": get_trashed,
        "all": get_all,
        "due": get_due,
        "lint": get_lint,
        "empty": get_empty_projects,
        "cleanup": get_cleanup
    }
