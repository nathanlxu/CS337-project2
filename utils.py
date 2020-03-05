from fractions import Fraction
import re

def scale_fractional_quantity(string, amt):
    allowed = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if not any(a in string for a in allowed):
        return string

    string = re.sub("[(\[].*?[)\]]", "", string)

    allowed += '/'
    allowed += ' '
    parsed_string = ''
    for s in string:
        if s in allowed:
            parsed_string += s

    flt = float(sum(Fraction(ps) for ps in parsed_string.split()))
    new_qty = round(amt * flt, 2)

    if int(new_qty) == new_qty and isinstance(new_qty, float):
        res = string.replace(parsed_string.strip(), str(int(new_qty)))
    else:
        res = string.replace(parsed_string.strip(), str(new_qty))

    return res