"""
Hardcoded list of common English nouns for use as codewords.
"""

import random
from typing import List


# High-frequency English nouns (common, simple words)
CODEWORDS: List[str] = [
    "pizza", "pasta", "computer", "phone", "car", "house", "book", "table",
    "chair", "door", "window", "tree", "water", "food", "time", "day",
    "year", "person", "man", "woman", "child", "friend", "family", "work",
    "school", "student", "teacher", "doctor", "lawyer", "engineer", "artist",
    "music", "song", "movie", "game", "sport", "football", "basketball",
    "tennis", "swimming", "running", "walking", "reading", "writing",
    "cooking", "eating", "sleeping", "travel", "vacation", "hotel",
    "restaurant", "coffee", "tea", "beer", "wine", "bread", "cheese",
    "apple", "banana", "orange", "strawberry", "chocolate", "cake",
    "money", "bank", "store", "shop", "market", "price", "cost",
    "city", "country", "world", "earth", "ocean", "mountain", "river",
    "beach", "forest", "park", "garden", "flower", "bird", "dog", "cat",
    "horse", "fish", "animal", "plant", "sun", "moon", "star", "sky",
    "cloud", "rain", "snow", "wind", "fire", "ice", "stone", "rock",
    "paper", "pen", "pencil", "desk", "lamp", "light", "color",
    "number", "letter", "word", "sentence", "story", "idea", "thought",
    "feeling", "emotion", "love", "happiness", "hope", "dream", "goal",
    "plan", "problem", "solution", "answer", "question", "knowledge",
    "information", "data", "fact", "truth", "secret", "power", "strength",
    "health", "medicine", "hospital", "office", "building", "room",
    "kitchen", "bathroom", "bedroom", "clothes", "shirt", "pants",
    "shoes", "hat", "jacket", "bag", "wallet", "key", "box", "tool",
    "machine", "device", "system", "network", "internet", "website",
    "email", "message", "call", "meeting", "event", "party", "holiday",
    "culture", "language", "history", "past", "present", "future",
    "beginning", "end", "start", "finish", "change", "difference",
]


def get_random_codeword() -> str:
    """Get a random codeword from the list."""
    return random.choice(CODEWORDS)


def get_codewords(count: int) -> List[str]:
    """Get multiple random codewords (with replacement)."""
    return [get_random_codeword() for _ in range(count)]
