import logging
import unittest

import HTMLTestRunner

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class BasicTestCase(unittest.TestCase):
    def test_one(self):
        logger.info('Test message 1!')
        self.assertEqual(1, 1)

    def test_two(self):
        """Extended description"""
        logger.error('Test message 1!')
        self.assertEqual(2, 2)


if __name__ == '__main__':
    import sys
    logging.basicConfig(stream=sys.stderr)

    with open('report.html', 'w') as report_file:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=report_file,
            title='Test Report',
            description='Regression Test Suite',
            verbosity=3,
            logger=logger
        )

        suite = unittest.TestLoader().loadTestsFromTestCase(BasicTestCase)

        result = runner.run(suite)
        print(result)