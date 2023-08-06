import io
import logging
import sys
import unittest
import random
import json
from collections import OrderedDict

from logger_json.formatter import JSONFormatter


class TestsLoggerJson(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("logging-test-{}".format(random.randint(1, 101)))
        self.logger.setLevel(logging.DEBUG)
        self.buffer = io.StringIO()

        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)

    def testDefaultFormat(self):
        fr = JSONFormatter()
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        log = logging.getLogger("TestLog")
        log.debug(self.buffer.getvalue())
        logJson = json.loads(self.buffer.getvalue())

        self.assertEqual(logJson["msg"], msg)

    def testUnknownFormatKey(self):
        fr = JSONFormatter(['unknown'])

        self.logHandler.setFormatter(fr)
        msg = "testing unknown logging format"
        try:
            self.logger.info(msg)
        except AttributeError:
            self.assertTrue(False, "Should succeed")

    def testOrderedDictFormat(self):
        fr = JSONFormatter()
        self.logHandler.setFormatter(fr)
        ordered_dict = OrderedDict((('user', 'Fred'), ('query', 'Bujold'), ('results', 5)))
        self.logger.info(ordered_dict)
        log = logging.getLogger("TestLog")
        log.debug(self.buffer.getvalue())
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json["msg"]["query"], "Bujold")
        self.assertEqual(log_json["msg"]["user"], "Fred")
        self.assertEqual(log_json["msg"]["results"], 5)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
if __name__ == '__main__':
    unittest.main()
