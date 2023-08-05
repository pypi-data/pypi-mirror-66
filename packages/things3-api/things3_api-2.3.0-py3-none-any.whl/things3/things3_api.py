#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only Things 3 Web Serivce."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.3.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
from os import getcwd
import json
from flask import Flask
from flask import Response
from werkzeug.serving import make_server
from things3.things3 import Things3


class Things3API():
    """API Wrapper for the simple read-only API for Things 3."""

    HOST = 'localhost'
    PORT = 15000
    PATH = getcwd() + '/resources/'
    things3 = None

    def on_get(self, url):
        """Handles other GET requests"""
        filename = self.PATH + url
        content_type = 'application/json'
        if filename.endswith('css'):
            content_type = 'text/css'
        if filename.endswith('html'):
            content_type = 'text/html'
        if filename.endswith('js'):
            content_type = 'text/javascript'
        if filename.endswith('png'):
            content_type = 'image/png'
        if filename.endswith('jpg'):
            content_type = 'image/jpeg'
        if filename.endswith('ico'):
            content_type = 'image/x-ico'
        with open(filename, 'rb') as source:
            data = source.read()
        return Response(response=data, content_type=content_type)

    def api(self, command):
        """Return database as JSON strings."""
        if command in self.things3.functions:
            func = self.things3.functions[command]
            data = json.dumps(
                self.things3.convert_tasks_to_model(func(self.things3)))
            return Response(response=data, content_type='application/json')

        data = json.dumps(self.things3.convert_tasks_to_model(
            self.things3.get_not_implemented()))
        return Response(response=data, content_type='application/json',
                        status=404)

    def __init__(self, database=None):
        self.things3 = Things3(database=database)
        self.flask = Flask(__name__)
        self.flask.add_url_rule('/api/<command>', view_func=self.api)
        self.flask.add_url_rule('/<url>', view_func=self.on_get)
        self.flask.app_context().push()
        self.flask_context = None

    def main(self):
        """"Main function."""
        print(f"Serving at http://{self.HOST}:{self.PORT} ...")

        try:
            self.flask_context = make_server(self.HOST, self.PORT, self.flask)
            self.flask_context.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down...")
            sys.exit(0)


def main():
    """Main entry point for CLI installation"""
    Things3API().main()


if __name__ == "__main__":
    main()
