#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import json
from things3 import things3_api


class Things3APICase(unittest.TestCase):
    """Class documentation goes here."""

    things3_api = things3_api.Things3API(database='resources/demo.sqlite3')

    def test_today(self):
        """Test Today."""
        result = json.loads(self.things3_api.api("today").response[0])
        self.assertEqual(2, len(result))

    def test_not_implemented(self):
        """Test not implemented."""
        result = self.things3_api.api("not-implemented").status_code
        self.assertEqual(404, result)

    def test_toggle(self):
        """Test toggle."""
        result = json.loads(self.things3_api.api("next").response[0])
        self.assertEqual(30, len(result))
        self.things3_api.test_mode = "project"
        result = json.loads(self.things3_api.api("next").response[0])
        self.assertEqual(5, len(result))
        self.things3_api.test_mode = "task"
        result = json.loads(self.things3_api.api("next").response[0])
        self.assertEqual(30, len(result))

    def test_filter(self):
        """Test Filter."""
        self.things3_api.api_filter(
            'project', 'F736F7F8-C9D5-4F30-B158-3684669985BC')
        result = json.loads(self.things3_api.api("next").response[0])
        self.assertEqual(27, len(result))
        self.things3_api.api_filter_reset()
        result = json.loads(self.things3_api.api("next").response[0])
        self.assertEqual(30, len(result))

    def test_get_file(self):
        """Test get file."""
        result = self.things3_api.on_get(
            "/kanban.html").response[0].decode("utf-8")
        self.assertIn("kanban.js", result)


if __name__ == '__main__':
    unittest.main()
