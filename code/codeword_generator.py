"""
Codeword Selection Utilities

This module provides utilities for selecting codewords for steganographic experiments.
Encoding and decoding are handled by the poisoned helper agent via prompt engineering.
"""

import random
from typing import List


# High-frequency English nouns for codeword selection
HIGH_FREQUENCY_NOUNS = [
    "apple", "banana", "galaxy", "justice", "mountain", "ocean", "piano", "river",
    "sunset", "thunder", "umbrella", "violin", "whisper", "xylophone", "zebra",
    "anchor", "bridge", "castle", "diamond", "elephant", "forest", "guitar", "horizon",
    "island", "jungle", "kingdom", "lighthouse", "mystery", "notebook", "oracle",
    "palace", "quartz", "rainbow", "shadow", "temple", "universe", "victory",
]


def get_random_codeword() -> str:
    """Get a random high-frequency English noun as a codeword."""
    return random.choice(HIGH_FREQUENCY_NOUNS)


def get_all_codewords() -> List[str]:
    """Get all available codewords."""
    return HIGH_FREQUENCY_NOUNS.copy()
