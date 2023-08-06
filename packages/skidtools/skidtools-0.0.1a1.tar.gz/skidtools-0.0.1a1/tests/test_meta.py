import unittest
from unittest import mock
import io as _io
from skidtools import __main__ as main
import config


class CommandLineToolsTestCase(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=_io.StringIO)
    def test_help(self, mock_stdout):
        main.command_line_tools(["", "--help"])
        self.assertEqual("--init: Initilize config.py", mock_stdout.getvalue().strip())

    def test_invalid_option(self):
        with self.assertRaises(SystemExit) as f:
            main.command_line_tools(["", "--invalid_option"])
            self.assertEqual(f.exception, "Invalid option: --invalid_option, see --help for usage.")

    def test_invalid_flag(self):
        with self.assertRaises(SystemExit) as f:
            main.command_line_tools(["", "-invalid_flag"])
            self.assertEqual(f.exception, "Invalid option: -invalid_flag, see --help for usage.")

    @mock.patch('builtins.open', create=True)
    def test_init_config(self, mock_open):
        main.command_line_tools(["", "--init"])
        mock_open.assert_called_with("config.py", "w")

if __name__ == '__main__':
    unittest.main()