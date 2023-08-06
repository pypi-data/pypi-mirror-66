import unittest
from unittest import mock
import io as _io
import config
from skidtools import slogging
import skidtools

class InitLoggingTestCase(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=_io.StringIO)
    def test_version(self, mock_stdout):
        slogging.init_logging(["", "--version"])
        self.assertEqual(f"version: {config.version}", mock_stdout.getvalue().strip())

    @mock.patch('sys.stdout', new_callable=_io.StringIO)
    def test_help(self, mock_stdout):
        slogging.init_logging(["", "--help"])
        self.assertEqual(config.help_text, mock_stdout.getvalue().strip())
        
    def test_invalid_option(self):
        with self.assertRaises(SystemExit) as f:
            slogging.init_logging(["", "--invalid_option"])
            self.assertEqual(f.exception, "Invalid option: --invalid_option, see --help for usage.")

    def test_invalid_flag(self):
        with self.assertRaises(SystemExit) as f:
            slogging.init_logging(["", "-invalid_flag"])
            self.assertEqual(f.exception, "Invalid option: -invalid_flag, see --help for usage.")


if __name__ == '__main__':
    unittest.main()