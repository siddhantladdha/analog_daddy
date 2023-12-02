import unittest
import sys
import os
from analog_daddy.importer import (
    read_pseudo_csv_file,
    CSVReadingError,
    strip_empty_strings,
    parse_value,
    extract_parameters_from_comment,
    separate_lines,
    process_parameters,
    create_data_structure,
    populate_data_values,
    nest_populated_dictionary,
)

class TestNestPopulatedDictionary(unittest.TestCase):

    def test_nest_populated_dictionary(self):
        # Input dictionaries
        x = {'ds': [0.0], 'gs': [0.0], 'length': [1e-06], 'sb': [0.0, 0.25]}
        y = {
            'cgg_nmos_svt': [[[[5.326e-14, 4.583e-14]]]], 
            'gm_nmos_svt': [[[[0.0, 0.0]]]], 
            'gmb_nmos_svt': [[[[0.0, 0.0]]]], 
            'gds_nmos_svt': [[[[4.232e-09, 1.381e-09]]]], 
            'id_nmos_svt': [[[[-0.0, 9.114e-17]]]], 
            'cgg_pmos_svt': [[[[8.263e-14, 7.165e-14]]]], 
            'gm_pmos_svt': [[[[0.0, 0.0]]]], 
            'gmb_pmos_svt': [[[[0.0, 0.0]]]], 
            'gds_pmos_svt': [[[[1.751e-10, 5.754e-11]]]], 
            'id_pmos_svt': [[[[-0.0, -1.569e-16]]]]
        }

        # Expected output
        expected_output = {
            'nmos_svt': {
                **x,
                'cgg': [[[[5.326e-14, 4.583e-14]]]],
                'gm': [[[[0.0, 0.0]]]],
                'gmb': [[[[0.0, 0.0]]]],
                'gds': [[[[4.232e-09, 1.381e-09]]]],
                'id': [[[[-0.0, 9.114e-17]]]]
            },
            'pmos_svt': {
                **x,
                'cgg': [[[[8.263e-14, 7.165e-14]]]],
                'gm': [[[[0.0, 0.0]]]],
                'gmb': [[[[0.0, 0.0]]]],
                'gds': [[[[1.751e-10, 5.754e-11]]]],
                'id': [[[[-0.0, -1.569e-16]]]]
            }
        }

        # Testing the function
        result = nest_populated_dictionary(y, x)
        self.assertEqual(result, expected_output)

class TestImporter(unittest.TestCase):
    maxDiff = None

    def test_populate_data_values(self):
        combined_lines = [
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
            ['cgg_nmos_svt', '53.26e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '4.232e-9'],
            ['id_nmos_svt', '-0'],
            ['cgg_pmos_svt', '82.63e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '175.1e-12'],
            ['id_pmos_svt', '-0'],
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m'],
            ['cgg_nmos_svt', '45.83e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '1.381e-9'],
            ['id_nmos_svt', '91.14e-18'],
            ['cgg_pmos_svt', '71.65e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '57.54e-12'],
            ['id_pmos_svt', '-156.9e-18']
        ]

        param_lines, data_lines = separate_lines(combined_lines)

        x = process_parameters(param_lines)
        y = create_data_structure(data_lines, x)

        populate_data_values(combined_lines, param_lines, x, y)

        expected_output = {
            'cgg_nmos_svt': [[[[53.26e-15, 45.83e-15]]]],
            'gm_nmos_svt': [[[[0.0, 0.0]]]],
            'gmb_nmos_svt': [[[[0.0, 0.0]]]],
            'gds_nmos_svt': [[[[4.232e-9, 1.381e-9]]]],
            'id_nmos_svt': [[[[0.0, 91.14e-18]]]],
            'cgg_pmos_svt': [[[[82.63e-15, 71.65e-15]]]],
            'gm_pmos_svt': [[[[0.0, 0.0]]]],
            'gmb_pmos_svt': [[[[0.0, 0.0]]]],
            'gds_pmos_svt': [[[[175.1e-12, 57.54e-12]]]],
            'id_pmos_svt': [[[[0.0, -156.9e-18]]]]
        }
        self.assertEqual(y, expected_output)

    def test_populate_data_values_empty_values(self):
        combined_lines = [
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
            ['cgg_nmos_svt', '53.26e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', ''],
            ['id_nmos_svt', '-0'],
            ['cgg_pmos_svt', '82.63e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', ''],
            ['id_pmos_svt', '-0'],
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m'],
            ['cgg_nmos_svt', '45.83e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '1.381e-9'],
            ['id_nmos_svt', '91.14e-18'],
            ['cgg_pmos_svt', '71.65e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '57.54e-12'],
            ['id_pmos_svt', '-156.9e-18']
        ]

        param_lines, data_lines = separate_lines(combined_lines)

        x = process_parameters(param_lines)
        y = create_data_structure(data_lines, x)

        populate_data_values(combined_lines, param_lines, x, y)

        expected_output = {
            'cgg_nmos_svt': [[[[53.26e-15, 45.83e-15]]]],
            'gm_nmos_svt': [[[[0.0, 0.0]]]],
            'gmb_nmos_svt': [[[[0.0, 0.0]]]],
            'gds_nmos_svt': [[[[123456789, 1.381e-9]]]],
            'id_nmos_svt': [[[[0.0, 91.14e-18]]]],
            'cgg_pmos_svt': [[[[82.63e-15, 71.65e-15]]]],
            'gm_pmos_svt': [[[[0.0, 0.0]]]],
            'gmb_pmos_svt': [[[[0.0, 0.0]]]],
            'gds_pmos_svt': [[[[123456789, 57.54e-12]]]],
            'id_pmos_svt': [[[[0.0, -156.9e-18]]]]
        }
        self.assertEqual(y, expected_output)

class TestCreateDataStructure(unittest.TestCase):

    def test_case_1(self):
        # Test Case 1
        input_data = [
            ['cgg_nmos_svt', '53.26e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '4.232e-9'],
            ['id_nmos_svt', '-0'],
            ['cgg_pmos_svt', '82.63e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '175.1e-12'],
            ['id_pmos_svt', '-0'],
            ['cgg_nmos_svt', '45.83e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '1.381e-9'],
            ['id_nmos_svt', '91.14e-18'],
            ['cgg_pmos_svt', '71.65e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '57.54e-12'],
            ['id_pmos_svt', '-156.9e-18']
        ]

        x = {
            'ds': [0],
            'gs': [0],
            'length': [1e-6],
            'sb': [0, 0.25]
        }
        expected_output = {
            'cgg_nmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'gm_nmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'gmb_nmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'gds_nmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'id_nmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'cgg_pmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'gm_pmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'gmb_pmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'gds_pmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']],
            'id_pmos_svt': [[[[None for _ in x['sb']] for _ in x['length']] for _ in x['gs']] for _ in x['ds']]
        }

        result = create_data_structure(input_data, x)
        self.assertEqual(result, expected_output)

class TestProcessParameters(unittest.TestCase):

    def test_case_1(self):
        # Test Case 1
        input_data = [
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m']
        ]

        expected_output = {
            'ds': [0],
            'gs': [0],
            'length': [1e-6],
            'sb': [0, 0.25]
        }

        result = process_parameters(input_data)
        self.assertEqual(result, expected_output)

class TestSeparateLines(unittest.TestCase):

    def test_case_1(self):
        # Test Case 1
        input_data = [
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
            ['cgg_nmos_svt', '53.26e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '4.232e-9'],
            ['id_nmos_svt', '-0'],
            ['cgg_pmos_svt', '82.63e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '175.1e-12'],
            ['id_pmos_svt', '-0'],
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m'],
            ['cgg_nmos_svt', '45.83e-15'],
            ['gm_nmos_svt', '0'],
            ['gmb_nmos_svt', '0'],
            ['gds_nmos_svt', '1.381e-9'],
            ['id_nmos_svt', '91.14e-18'],
            ['cgg_pmos_svt', '71.65e-15'],
            ['gm_pmos_svt', '0'],
            ['gmb_pmos_svt', '0'],
            ['gds_pmos_svt', '57.54e-12'],
            ['id_pmos_svt', '-156.9e-18']
        ]

        expected_output = (
            # Expected param_lines
            [
                ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
                ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m']
            ],
            # Expected data_lines
            [
                ['cgg_nmos_svt', '53.26e-15'],
                ['gm_nmos_svt', '0'],
                ['gmb_nmos_svt', '0'],
                ['gds_nmos_svt', '4.232e-9'],
                ['id_nmos_svt', '-0'],
                ['cgg_pmos_svt', '82.63e-15'],
                ['gm_pmos_svt', '0'],
                ['gmb_pmos_svt', '0'],
                ['gds_pmos_svt', '175.1e-12'],
                ['id_pmos_svt', '-0'],
                ['cgg_nmos_svt', '45.83e-15'],
                ['gm_nmos_svt', '0'],
                ['gmb_nmos_svt', '0'],
                ['gds_nmos_svt', '1.381e-9'],
                ['id_nmos_svt', '91.14e-18'],
                ['cgg_pmos_svt', '71.65e-15'],
                ['gm_pmos_svt', '0'],
                ['gmb_pmos_svt', '0'],
                ['gds_pmos_svt', '57.54e-12'],
                ['id_pmos_svt', '-156.9e-18']
            ]
        )

        result = separate_lines(input_data)
        self.assertEqual(result, expected_output)

class TestExtractParametersFromComment(unittest.TestCase):

    def test_basic_extraction(self):
        comment = ['Parameters:', 'ds=0, gs=0, length=1u, sb=0']
        expected = {
            'ds': '0',
            'gs': '0',
            'length': '1u',
            'sb': '0'
        }
        self.assertEqual(extract_parameters_from_comment(comment), expected)

    def test_empty_comment(self):
        comment = []
            
        with self.assertRaises(ValueError) as context:
            extract_parameters_from_comment(comment)
            
        self.assertEqual(str(context.exception), "The list is empty!")

    def test_no_parameters(self):
        comment = ['Parameters:', '']

        with self.assertRaises(ValueError) as context:
            extract_parameters_from_comment(comment)
        
        self.assertEqual(str(context.exception), "There are no parameters specified at all")

    def test_invalid_format(self):
        comment = ['Parameters', 'ds=0, gs=0, length=1u, sb=0'] # missing colon after Parameters
        expected = {}
        self.assertEqual(extract_parameters_from_comment(comment), expected)

class TestParseValue(unittest.TestCase):
    def test_parse_with_valid_prefixes(self):
        self.assertEqual(parse_value("1k"), 1000.0)
        self.assertEqual(parse_value("2.5M"), 2500000.0)
        self.assertEqual(parse_value("3u"), 0.000003)
        self.assertEqual(parse_value("4p"), 0.000000000004)
        self.assertEqual(parse_value("5a"), 0.000000000000000005)

    def test_parse_without_prefix(self):
        self.assertEqual(parse_value("42.5"), 42.5)
        self.assertEqual(parse_value("0.001"), 0.001)
        self.assertEqual(parse_value("123"), 123.0)

    def test_parse_invalid_input(self):
        with self.assertRaises(ValueError):
            parse_value("invalid")  # Non-numeric input should raise a ValueError
        with self.assertRaises(ValueError):
            parse_value("1x")  # Invalid prefix should raise a ValueError

class TestStripEmptyStrings(unittest.TestCase):

    def setUp(self):
        # Prepare the sample file path for testing
        self.sample_file_path = os.path.join("tests", "MVE.csv")

    def test_strip_empty_strings_for_file(self):
        # Test stripping empty strings from the sample file data
        data = read_pseudo_csv_file(self.sample_file_path)
        stripped_data = strip_empty_strings(data)
        # Define the expected data with empty strings and whitespaces removed, and "Parameters" line split
        expected_data_stripped = [
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
            ["cgg_nmos_svt", "53.26e-15"],
            ["gm_nmos_svt", "0"],
            ["gmb_nmos_svt", "0"],
            ["gds_nmos_svt", "4.232e-9"],
            ["id_nmos_svt", "-0"],
            ["cgg_pmos_svt", "82.63e-15"],
            ["gm_pmos_svt", "0"],
            ["gmb_pmos_svt", "0"],
            ["gds_pmos_svt", "175.1e-12"],
            ["id_pmos_svt", "-0"],
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m'],
            ["cgg_nmos_svt", "45.83e-15"],
            ["gm_nmos_svt", "0"],
            ["gmb_nmos_svt", "0"],
            ["gds_nmos_svt", "1.381e-9"],
            ["id_nmos_svt", "91.14e-18"],
            ["cgg_pmos_svt", "71.65e-15"],
            ["gm_pmos_svt", "0"],
            ["gmb_pmos_svt", "0"],
            ["gds_pmos_svt", "57.54e-12"],
            ["id_pmos_svt", "-156.9e-18"],
        ]

        # Add an assertion to check if empty strings and whitespaces are removed as expected
        self.assertEqual(stripped_data, expected_data_stripped)

class TestReadPseudoCSVFile(unittest.TestCase):

    def setUp(self):
        # Prepare the sample file path for testing
        self.sample_file_path = os.path.join("tests", "MVE.csv")
    
    def test_file_not_found(self):
        with self.assertRaises(CSVReadingError) as context:
            read_pseudo_csv_file("non_existent_file.csv")
        
        self.assertTrue("The file 'non_existent_file.csv' was not found." in str(context.exception))

    def test_read_valid_file(self):
        test_file_name = "input.csv"
        try:
            # Given a sample input.csv
            with open(test_file_name, "w") as f:
                f.write("Header1,Header2\n")
                f.write("Row1Col1,Row1Col2\n")
                f.write("Row2Col1,Row2Col2\n")

            expected_output = [
                ["Row1Col1", "Row1Col2"],
                ["Row2Col1", "Row2Col2"]
            ]
            result = read_pseudo_csv_file(test_file_name)
            self.assertEqual(result, expected_output)
        finally:
            # Cleanup: remove the file
            if os.path.exists(test_file_name):
                os.remove(test_file_name)

                
    def test_parameters_handling(self):
        test_file_name = "input_with_parameters.csv"
        try:
            # Given a sample input_with_parameters.csv
            with open(test_file_name, "w") as f:
                f.write("Header1,Header2\n")
                f.write("Parameters: ds=5\n")
                f.write("Row1Col1,Row1Col2\n")
                f.write("Row2Col1,Row2Col2\n")

            expected_output = [
                ["Parameters:", "ds=5"],
                ["Row1Col1", "Row1Col2"],
                ["Row2Col1", "Row2Col2"]
            ]
            result = read_pseudo_csv_file("input_with_parameters.csv")
            self.assertEqual(result, expected_output)
        finally:
            # Cleanup: remove the file
            if os.path.exists(test_file_name):
                os.remove(test_file_name)
    
    def test_read_pseudo_csv_file(self):
        # Test reading the sample file
        data = read_pseudo_csv_file(self.sample_file_path)
        expected_data = [
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=0'],
            ["1", "dc_sweep", "cgg_nmos_svt", "53.26e-15", "", "", ""],
            ["1", "dc_sweep", "gm_nmos_svt", "0", "", "", ""],
            ["1", "dc_sweep", "gmb_nmos_svt", "0", "", "", ""],
            ["1", "dc_sweep", "gds_nmos_svt", "4.232e-9", "", "", ""],
            ["1", "dc_sweep", "id_nmos_svt", "-0", "", "", ""],
            ["1", "dc_sweep", "cgg_pmos_svt", "82.63e-15", "", "", ""],
            ["1", "dc_sweep", "gm_pmos_svt", "0", "", "", ""],
            ["1", "dc_sweep", "gmb_pmos_svt", "0", "", "", ""],
            ["1", "dc_sweep", "gds_pmos_svt", "175.1e-12", "", "", ""],
            ["1", "dc_sweep", "id_pmos_svt", "-0", "", "", ""],
            ['Parameters:', 'ds=0, gs=0, length=1u, sb=250m'],
            ["2", "dc_sweep", "cgg_nmos_svt", "45.83e-15", "", "", ""],
            ["2", "dc_sweep", "gm_nmos_svt", "0", "", "", ""],
            ["2", "dc_sweep", "gmb_nmos_svt", "0", "", "", ""],
            ["2", "dc_sweep", "gds_nmos_svt", "1.381e-9", "", "", ""],
            ["2", "dc_sweep", "id_nmos_svt", "91.14e-18", "", "", ""],
            ["2", "dc_sweep", "cgg_pmos_svt", "71.65e-15", "", "", ""],
            ["2", "dc_sweep", "gm_pmos_svt", "0", "", "", ""],
            ["2", "dc_sweep", "gmb_pmos_svt", "0", "", "", ""],
            ["2", "dc_sweep", "gds_pmos_svt", "57.54e-12", "", "", ""],
            ["2", "dc_sweep", "id_pmos_svt", "-156.9e-18", "", "", ""],
        ]
        # Perform the assertion to check if the data matches the expected data
        self.assertEqual(data, expected_data)