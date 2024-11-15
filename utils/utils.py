#!/usr/bin/env python3

import os, sys
import time

ROOT = os.path.abspath(os.path.dirname(os.path.join(__file__, "../../")))
sys.path.append(ROOT)


def path_check(path_in: str) -> bool:
    if not os.path.exists(path_in):
        print(f'[Error] path {path_in} not found\n')
        return False
    return True
