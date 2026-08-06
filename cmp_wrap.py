#!/usr/bin/env python3
"""cmpparts with a local workaround for numeric part names (e.g. '8080').

kipart.compare_parts._normalize() calls name.lower(), which blows up when the
s-expression reader hands back an int for a purely numeric symbol name.
"""
import re
import sys

from kipart import compare_parts as cp

_orig = cp._normalize
cp._normalize = lambda name: re.sub(r"[^0-9a-z]", "", str(name).lower())
cp.name_similarity.__globals__["_normalize"] = cp._normalize

sys.exit(cp.cmpparts())
