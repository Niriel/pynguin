#! /usr/bin/python
"""
Created on Jan 9, 2011

@author: Niriel
"""
import os
import sys
import unittest

def ImportModule(file_name):
    """Import the module specified by file_name."""
    file_name = os.path.splitext(file_name)[0][2:]
    file_name = file_name.replace(os.sep, '.')
    __import__(file_name)
    return sys.modules[file_name]

def visit(suites, dirname, names):
    to_process = [name for name in names if (name.startswith('test_') and
                                             name.endswith('.py'))]
    print dirname, to_process
    for name in to_process:
        full_name = os.path.join(dirname, name)
        module = ImportModule(full_name)
        suites.append(unittest.TestLoader().loadTestsFromModule(module))

def GatherSuites():
    suites = []
    os.path.walk('.', visit, suites)
    return suites

def main():
    suite = unittest.TestSuite(GatherSuites())
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    main()
