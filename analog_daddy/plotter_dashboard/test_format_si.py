import unittest
from parse_si import format_si_or_scientific

class TestFormatSI(unittest.TestCase):
    def test_format_si_cases(self):
        test_cases = [
            (0.01, 'si', {}, '10m'),
            (2000.0, 'si', {}, '2k'),
            (0.001, 'si', {}, '1m'),
            (5.0, 'si', {}, '5'),
            (-3_500_000.0, 'si', {}, '-3.5M'),
            (0.5e-6, 'si', {}, '500n'),
            (1e11, 'si', {}, '100G'),
            (7.2e-12, 'si', {}, '7.2p'),
            (-1.2e12, 'si', {}, '-1.2T'),
            (3.3e-9, 'si', {}, '3.3n'),
            (0.0, 'si', {}, '0'),
            (4.2, 'si', {}, '4.2'),
            (123.0, 'si', {}, '123'),
            (0.0123, 'si', {}, '12.3m'),
            (0.00123, 'scientific', {}, '1.230000e-03'),
            (1000, 'scientific', {}, '1.000000e+03'),
            (0.00042, 'scientific', {}, '4.200000e-04'),
            (-0.00042, 'si', {}, '-420u'),
            (-4200, 'si', {}, '-4.2k'),
            (1e-3, 'si', {}, '1m'),
            (1e3, 'si', {}, '1k'),
            (1e6, 'si', {}, '1M'),
            (1e-16, 'si', {}, '0.1f'),
            (-1e-16, 'si', {}, '-0.1f'),
            (1e15, 'si', {}, '1000T'),
            (-1e15, 'si', {}, '-1000T'),
            (0.1, 'si', {}, '100m'),
            (0.2, 'si', {}, '200m'),
            (1234567.89, 'si', {'precision': 6}, '1.23457M'),
            (1, 'si', {}, '1'),
            (-1, 'si', {}, '-1'),
            (0, 'scientific', {}, '0'),
            (5.433434343e-07, 'si', {'precision': 2}, '543.34n'),
            (5.40e-07, 'si', {'precision': 2}, '540n'),
            (5.402e-07, 'si', {'precision': 2}, '540.2n'),
        ]
        for value, style, kwargs, expected in test_cases:
            result = format_si_or_scientific(value, style, **kwargs)
            print(f"Test: value={value}, style={style}, kwargs={kwargs} -> result={result}, expected={expected}")
            self.assertEqual(result, expected, f"Failed: {value}, {style}, {kwargs} -> {result}, expected {expected}")

if __name__ == "__main__":
    unittest.main()
