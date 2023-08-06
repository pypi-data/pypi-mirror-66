"""Library for generating and embedding test data.

Python library for generating and embedding in a compact way
random but reproducible data for unit testing.
"""

from __future__ import annotations
from typing import Sequence
from math import log2
from hashlib import sha256
import doctest

class fountains():
    """
    Class for test data enumeration objects.
    
    >>> f = fountains(2)
    >>> [int.from_bytes(bs, 'little') for (_, bs) in zip(range(3), f)]
    [45283, 7118, 54574]
    >>> f = fountains(1, 3)
    >>> [int.from_bytes(bs, 'little') for bs in f]
    [227, 206, 46]
    """

    def __init__(self, length = 1, limit = None, seed = bytes(0)):
        self.length = length
        self.limit = limit
        self.count = 0
        if isinstance(seed, int):
            self.state = seed.to_bytes(int(log2(seed)) // 8, 'little')
        elif isinstance(seed, str):
            self.state = str.encode(seed)
        elif isinstance(seed, bytes) or isinstance(seed, bytearray):
            self.state = seed
        else:
            raise ValueError("seed must be of type int, str, bytes, or bytearray")

    def __iter__(self):
        while self.limit is None or self.count < self.limit:
            bs = bytearray()
            while len(bs) < self.length:
                bs_ = sha256(self.state).digest()
                bs.extend(bs_[:16])
                self.state = bs_[16:]
            self.count += 1
            yield bs[:self.length]

if __name__ == "__main__":
    doctest.testmod()
