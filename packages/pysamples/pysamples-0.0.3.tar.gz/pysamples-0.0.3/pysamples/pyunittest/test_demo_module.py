#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import HTMLReport
import unittest
import test_demo_class
from test_demo_class import TestDemo


if __name__ == '__main__':
    paras = sys.argv[1:]
    args = paras[0]
    report = paras[1]

    suite = unittest.TestSuite()
    if args == 'test':
        tests = [TestDemo("test_minus"), TestDemo("test_add"), TestDemo("test_minus_with_skip")]
        suite.addTests(tests)
    elif args == 'tests':
        suite.addTest(TestDemo("test_minus"))
        suite.addTest(TestDemo("test_add"))
        suite.addTest(TestDemo("test_minus_with_skip"))
    elif args == 'class':
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDemo))
    elif args == 'module':
        suite.addTests(unittest.TestLoader().loadTestsFromModule(test_demo_class))
    elif args == 'mix':
        suite.addTests(unittest.TestLoader().loadTestsFromName('test_demo_class.TestDemo.test_minus'))
    elif args == 'mixs':
        suite.addTests(unittest.TestLoader().loadTestsFromNames(['test_demo_class.TestDemo.test_minus', 'test_demo_class.TestDemo', 'test_demo_class']))
    elif args == 'discover':
        suite.addTests(unittest.TestLoader().discover('.', 'test_*.py', top_level_dir=None))

    if report == 'terminal':
        runner = unittest.TextTestRunner(verbosity=1)
        runner.run(suite)
    elif report == 'txt':
        with open('ut_log.txt', 'a') as fp:
            runner = unittest.TextTestRunner(stream=fp, verbosity=1)
            runner.run(suite)
    elif report == 'html':
        runner = HTMLReport.TestRunner(report_file_name='test',
                               output_path='report',
                               title='测试报告',
                               description='测试描述',
                               sequential_execution=True
                               )
        runner.run(suite)