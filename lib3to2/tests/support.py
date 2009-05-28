"""Support code for test_*.py files"""

# Python imports
import unittest
import sys
import os
import os.path
import re
from itertools import chain
from operator import itemgetter
from textwrap import dedent

import refactor
from lib2to3 import pygram, pytree, fixer_util
from lib2to3.pgen2 import driver

test_dir = os.path.dirname(__file__)
proj_dir = os.path.normpath(os.path.join(test_dir, ".."))
grammar_path = os.path.join(test_dir, "..", "Grammar.txt")
grammar = driver.load_grammar(grammar_path)
driver = driver.Driver(grammar, convert=pytree.convert)

def parse_string(string):
    return driver.parse_string(reformat(string), debug=True)

def run_all_tests(test_mod=None, tests=None):
    if tests is None:
        tests = unittest.TestLoader().loadTestsFromModule(test_mod)
    unittest.TextTestRunner(verbosity=2).run(tests)

def reformat(string):
    return dedent(string) + u"\n\n"

def get_refactorer(fixers=None, options=None):
    """
    A convenience function for creating a RefactoringTool for tests.

    fixers is a list of fixers for the RefactoringTool to use. By default
    "lib2to3.fixes.*" is used. options is an optional dictionary of options to
    be passed to the RefactoringTool.
    """
    if fixers is not None:
        fixers = ["lib3to2.fixes.fix_" + fix for fix in fixers]
    else:
        fixers = refactor.get_fixers_from_package("lib3to2.fixes")
    options = options or {}
    return refactor.RefactoringTool(fixers, options, explicit=True)

def all_project_files():
    for dirpath, dirnames, filenames in os.walk(proj_dir):
        for filename in filenames:
            if filename.endswith(".py") and filename.startswith("test_"):
                yield os.path.join(dirpath, filename)

TestCase = unittest.TestCase
