#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import re

"""
Miniature version of cpython's Tools/scripts/h2py.py just good
enough to parse constants from Gianguido Sora's usb_hid_keys.h
"""


def parse(file):
    for rline in file:
        if not rline.startswith("#define "):
            continue

        line = rline.strip()

        comment = None

        if '//' in line:
            (line, comment) = line.split("//", maxsplit=1)

        try:
            (_, constant_name, value) = line.split(" ", maxsplit=2)
        except ValueError:
            continue

        if constant_name[0:4] == "KEY_":
            constant_name = constant_name[4:]

        out = '    "%s": %s,' % (constant_name, value.strip())
        if comment:
            out += "  # %s" % comment.strip()

        yield out


if __name__ == "__main__":
    with open("6da26e382a7ad91b5496ee55fdc73db2/usb_hid_keys.h", "r") as f:

        print("#!/usr/bin/env python")
        print("# -*- coding: utf-8 -*-")
        print("# Auto-generated from 6da26e382a7ad91b5496ee55fdc73db2/usb_hid_keys.h with generate_scancodes.py")
        print()
        print("KEY = {")
        for out in parse(f):
            print(out)
        print("}")