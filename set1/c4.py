from itertools import chain
from typing import List

from .c3 import *


def try_all_inputs(file_name: str) -> List[bytes]:
    inputs = open(file_name).readlines()
    return list(chain(*[try_all_xor_hex(f) for f in inputs]))
