from parse_si import parse_text_for_si_prefix

test_cases = [
    ("10m", 0.01),
    ("2k", 2000.0),
    ("1e-3", 0.001),
    ("5", 5.0),
    ("-3.5M", -3_500_000.0),
    ("0.5u", 0.5e-6),
    ("100G", 1e11),
    ("7.2p", 7.2e-12),
    ("-1.2T", -1.2e12),
    ("3.3n", 3.3e-9),
    ("0", 0.0),
    ("+4.2", 4.2),
    ("1.23e2", 123.0),
    ("1.23e-2", 0.0123),
    ("badinput", None),
    ("", None),
    ("1.2x", None),
    ("z15", None),
    ("m15", None),
]

for s, expected in test_cases:
    result = parse_text_for_si_prefix(s)
    if expected is None:
        assert result is None, f"Failed: {s} -> {result}, expected None"
    else:
        assert abs(result - expected) < 1e-12, f"Failed: {s} -> {result}, expected {expected}"
    print(f"Passed: {s} -> {result}")

print("All tests passed!")
