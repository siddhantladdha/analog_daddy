import re

def parse_text_for_scientific_or_si_prefix(value):
    """
    Parse a string with an SI prefix or scientific notation and return its float value.
    E.g., '10m' -> 0.01, '2k' -> 2000.0, '1e-3' -> 0.001
    Returns None if parsing fails.
    """
    si_dict = {
        'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3,
        '': 1, 'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12
    }
    value = value.strip()
    # Try to parse as float (handles scientific notation)
    try:
        return float(value)
    except ValueError:
        pass
    # Try to parse as SI-prefixed value
    match = re.fullmatch(r'([-+]?[0-9]*\.?[0-9]+)\s*([fpnumkMGT]?)', value)
    if match:
        number, prefix = match.groups()
        return float(number) * si_dict.get(prefix, 1)
    else:
        return None

def format_si_or_scientific(value, style='si', precision=6):
    """
    Format a float as an SI-prefixed string or scientific notation.
    style: 'si' (default) or 'scientific'
    precision: number of significant digits for mantissa
    """
    if value == 0:
        return "0"
    si_prefixes = [
        (1e12, 'T'), (1e9, 'G'), (1e6, 'M'), (1e3, 'k'), (1, ''),
        (1e-3, 'm'), (1e-6, 'u'), (1e-9, 'n'), (1e-12, 'p'), (1e-15, 'f')
    ]
    if style == 'scientific':
        return f"{value:.{precision}e}"
    # SI formatting
    abs_val = abs(value)
    for factor, prefix in si_prefixes:
        if abs_val >= factor or factor == 1e-15:
            mantissa = value / factor
            if mantissa == int(mantissa):
                mantissa_str = str(int(mantissa))
            else:
                mantissa_str = f"{mantissa:.{precision}g}"
            return f"{mantissa_str}{prefix}"
    return str(value)
