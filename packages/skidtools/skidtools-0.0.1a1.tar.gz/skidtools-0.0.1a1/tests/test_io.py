import unittest
from unittest import mock
import io as _io
from skidtools import sio

class ColoredPrintTestCase(unittest.TestCase):

    def test_raise_error(self):
        self.assertRaises(ValueError, sio.colored_print, "test text", "invalid color")

    def test_construct_string(self):
        self.assertEqual(sio.colored_print("test text", "green"), "\x1b[32mtest text\x1b[0m")

class ValidatedInputTestCase(unittest.TestCase):

    def invalid_type(self):
        pass

    def test_invalid_type(self):
        self.assertRaises(ValueError, sio.validated_input, "test text", self.invalid_type)

    @mock.patch("builtins.input", return_value="1234")
    def test_conversion_int(self, input):
        self.assertEqual(sio.validated_input("test text", int), 1234)

    @mock.patch("builtins.input", return_value="234.466")
    def test_conversion_float(self, input):
        self.assertEqual(sio.validated_input("test text", float), 234.466)

    @mock.patch("builtins.input", return_value="a string")
    def test_conversion_str(self, input):
        self.assertEqual(sio.validated_input("test text", str), "a string")

class LoadCombosTestCase(unittest.TestCase):

    @mock.patch('builtins.open', create=True)
    def test_load_combos(self, mock_open):
        sio.load_combos()
        mock_open.assert_called_with("combos.txt", "r")

 
if __name__ == '__main__':
    unittest.main()