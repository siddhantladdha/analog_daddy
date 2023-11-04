"""
This is a sample test for write_config, you can expand it based on your needs.
"""
import unittest
from unittest.mock import patch
from io import StringIO
from analog_daddy.write_config import (prompt_natural_number,
                                       prompt_float,
                                       prompt_bool,
                                       prompt_string,
                                       write_config)

class TestConfigPromptFunctions(unittest.TestCase):

    def test_prompt_natural_number(self):
        with patch('builtins.input', return_value='5'):
            self.assertEqual(prompt_natural_number('Enter a number', 10), 5)
        with patch('builtins.input', return_value=''):
            self.assertEqual(prompt_natural_number('Enter a number', 10), 10)
        with patch('builtins.input', side_effect=['0', '5']):
            self.assertEqual(prompt_natural_number('Enter a number', 10), 5)

        # Test invalid input with error message
        with patch('builtins.input', side_effect=['0', '5']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.assertEqual(prompt_natural_number('Enter a number', 10), 5)
                self.assertIn("Invalid input. Please provide a valid natural number.", mock_stdout.getvalue())

    def test_prompt_float(self):
        with patch('builtins.input', return_value='5.5'):
            self.assertEqual(prompt_float('Enter a float', 10.5), 5.5)
        with patch('builtins.input', return_value=''):
            self.assertEqual(prompt_float('Enter a float', 10.5), 10.5)
        with patch('builtins.input', side_effect=['-0.5', '5.5']):
            self.assertEqual(prompt_float('Enter a float', 10.5, min_val=0.1), 5.5)

    def test_prompt_bool(self):
        with patch('builtins.input', return_value='yes'):
            self.assertTrue(prompt_bool('Enter a bool', True))
        with patch('builtins.input', return_value='no'):
            self.assertFalse(prompt_bool('Enter a bool', False))

    def test_prompt_string(self):
        with patch('builtins.input', return_value='hello'):
            self.assertEqual(prompt_string('Enter a string', 'world'), 'hello')
        with patch('builtins.input', return_value=''):
            self.assertEqual(prompt_string('Enter a string', 'world'), 'world')

    # def test_write_config(self):
    #     # This is a sample test for write_config, you can expand it based on your needs.
    #     with patch('builtins.input', side_effect=['param', 'gm_',
    #                                               'length', 'gs',
    #                                               'ds', 'sb', 'db',
    #                                               'gb', 'method', 'warning',
    #                                               '1', 'true', '2', '4',
    #                                               '3', '5', '0.02', 'false']):
    #         with patch('builtins.open', unittest.mock.mock_open()) as m:
    #             write_config('conf.py')
    #             m.assert_called_once_with('conf.py', 'w', encoding='utf-8')