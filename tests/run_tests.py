import unittest
import HtmlTestRunner

test_loader = unittest.TestLoader()
test_suite = test_loader.discover('tests', pattern='test_*.py')

runner = HtmlTestRunner.HTMLTestRunner(output='reports')
runner.run(test_suite)