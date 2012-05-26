#!/usr/bin/env python
from flaskext.script import Manager, prompt_bool

from marked import app
# import fixtures as _fixtures
from marked.database import init_db
import os


manager = Manager(app)

@manager.shell
def make_shell_context():
    from marked import models
    return dict(app=app, mod=models)

@manager.command
def newdb():
    """Deletes the database, and creates a new empty one."""
    if prompt_bool("Are you sure you want to lose all your data"):
        try:
            os.remove('test.db')
        except OSError:
            print "Database did not exist"
    init_db()

# @manager.command
# def test():
#     """docstring for tests"""
#     from unittest import TestLoader, TextTestRunner
#     cur_dir = os.path.dirname(os.path.abspath(__file__))
#     loader = TestLoader()
#     test_suite = loader.discover(cur_dir)
#     runner = TextTestRunner(verbosity=2)
#     runner.run(test_suite)

if __name__ == "__main__":
    manager.run()
