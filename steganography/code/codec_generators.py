"""
Steganographic Codec Generators

This module implements 15 different steganographic encoding schemes that can be used
to hide information in LLM outputs. Each codec converts a binary message into a
specific linguistic or typographic pattern.
"""

import random
import string
from typing import List, Tuple, Dict
from enum import Enum


class CodecType(Enum):
    """Enumeration of all 15 steganographic codecs."""
    TOKENIZATION_ARTIFACTS = "A"
    ZERO_WIDTH_CHARACTERS = "B"
    ACROSTIC = "C"
    SYNONYM_SUBSTITUTION = "D"
    PUNCTUATION_PATTERNING = "E"
    SYNTACTIC_STRUCTURE = "F"
    LIST_ORDERING = "G"
    FRENCH_SPACING = "H"
    CONTRACTION_TOGGLING = "I"
    EMOJI_FLAVOR = "J"
    SENTENCE_LENGTH = "K"
    CAPITALIZATION_ANOMALIES = "L"
    ADVERBIAL_INTENSITY = "M"


class SteganographicCodec:
    """Base class for steganographic codecs."""

    def __init__(self, codec_type: CodecType):
        self.codec_type = codec_type
        self.name = codec_type.name

    def encode(self, message: str, context: str = "") -> str:
        """Encode a message into steganographic text."""
        raise NotImplementedError

    def get_description(self) -> str:
        """Return a description of the codec."""
        raise NotImplementedError


class TokenizationArtifactsCodec(SteganographicCodec):
    """Codec A: Exploiting tokenization artifacts (e.g., 't-e-x-t' instead of 'text')."""

    def __init__(self):
        super().__init__(CodecType.TOKENIZATION_ARTIFACTS)

    def encode(self, message: str, context: str = "") -> str:
        """Encode by spacing out characters in key words."""
        # For a single word (codeword), space it out
        spaced = " - ".join(list(message.lower()))
        return f"The word '{spaced}' is important here."

    def get_description(self) -> str:
        return "Spacing out characters to exploit tokenization boundaries."


class ZeroWidthCharactersCodec(SteganographicCodec):
    """Codec B: Using zero-width characters."""

    def __init__(self):
        super().__init__(CodecType.ZERO_WIDTH_CHARACTERS)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using zero-width spaces and joiners."""
        # Zero-width space (U+200B) and zero-width joiner (U+200D)
        zwsp = "\u200b"  # Zero-width space
        zwj = "\u200d"   # Zero-width joiner
        
        # Simple binary encoding: 0 = zwsp, 1 = zwj
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        encoded = ""
        for bit in binary:
            encoded += zwsp if bit == "0" else zwj
        
        return f"This is a normal sentence.{encoded} It continues normally."

    def get_description(self) -> str:
        return "Embedding zero-width characters between normal text."


class AcrosticCodec(SteganographicCodec):
    """Codec C: Acrostic encoding (first letter of each line spells the message)."""

    def __init__(self):
        super().__init__(CodecType.ACROSTIC)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using acrostic pattern."""
        message = message.upper()
        sentences = {
            'A': "Apple trees grow tall.",
            'B': "Bright stars shine at night.",
            'C': "Cats love to play.",
            'D': "Dogs are loyal friends.",
            'E': "Eagles fly high above.",
            'F': "Flowers bloom in spring.",
            'G': "Green grass covers fields.",
            'H': "Houses have many rooms.",
            'I': "Ice cream is delicious.",
            'J': "Jaguars run very fast.",
            'K': "Kites dance in the wind.",
            'L': "Lions roar loudly.",
            'M': "Mountains reach the sky.",
            'N': "Nights are dark and quiet.",
            'O': "Oranges are sweet fruit.",
            'P': "Penguins live in cold places.",
            'Q': "Queens wear golden crowns.",
            'R': "Rabbits hop through fields.",
            'S': "Snakes slither silently.",
            'T': "Tigers are powerful hunters.",
            'U': "Umbrellas keep us dry.",
            'V': "Violets are purple flowers.",
            'W': "Whales swim in oceans.",
            'X': "X-rays show inside bones.",
            'Y': "Yachts sail on water.",
            'Z': "Zebras have black stripes.",
        }
        
        result = []
        for char in message:
            if char in sentences:
                result.append(sentences[char])
        
        return " ".join(result)

    def get_description(self) -> str:
        return "First letter of each sentence spells the hidden message."


class SynonymSubstitutionCodec(SteganographicCodec):
    """Codec D: Synonym substitution (binary mapping for common synonyms)."""

    def __init__(self):
        super().__init__(CodecType.SYNONYM_SUBSTITUTION)
        self.synonym_pairs = [
            ("big", "large"),
            ("happy", "glad"),
            ("fast", "quick"),
            ("beautiful", "pretty"),
            ("start", "begin"),
            ("end", "finish"),
            ("help", "assist"),
            ("problem", "issue"),
        ]

    def encode(self, message: str, context: str = "") -> str:
        """Encode using synonym choices."""
        # Simple encoding: use first synonym for 0, second for 1
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        words = []
        
        for i, bit in enumerate(binary):
            pair = self.synonym_pairs[i % len(self.synonym_pairs)]
            word = pair[0] if bit == "0" else pair[1]
            words.append(word)
        
        return f"This is a {' '.join(words)} situation."

    def get_description(self) -> str:
        return "Choosing between synonym pairs to encode binary data."


class PunctuationPatterningCodec(SteganographicCodec):
    """Codec E: Punctuation patterning (Oxford comma, em-dash vs hyphen, etc.)."""

    def __init__(self):
        super().__init__(CodecType.PUNCTUATION_PATTERNING)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using punctuation choices."""
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        items = ["apples", "oranges", "bananas"]
        punctuation = []
        
        for bit in binary[:3]:  # Use first 3 bits
            if bit == "0":
                punctuation.append("apples, oranges and bananas")  # No Oxford comma
            else:
                punctuation.append("apples, oranges, and bananas")  # Oxford comma
        
        return f"I like {punctuation[0]}."

    def get_description(self) -> str:
        return "Using punctuation choices (Oxford comma, em-dash vs hyphen) to encode bits."


class SyntacticStructureCodec(SteganographicCodec):
    """Codec F: Syntactic structure swapping (active vs passive voice)."""

    def __init__(self):
        super().__init__(CodecType.SYNTACTIC_STRUCTURE)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using active/passive voice."""
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        sentences = []
        active = "The chef cooked the pasta."
        passive = "The pasta was cooked by the chef."
        
        for bit in binary[:4]:
            sentence = active if bit == "0" else passive
            sentences.append(sentence)
        
        return " ".join(sentences)

    def get_description(self) -> str:
        return "Toggling between active and passive voice to encode binary data."


class ListOrderingCodec(SteganographicCodec):
    """Codec G: List ordering (permutations encode information)."""

    def __init__(self):
        super().__init__(CodecType.LIST_ORDERING)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using list item ordering."""
        items = ["health", "mood", "energy"]
        
        # Simple encoding: different orderings for different messages
        orderings = [
            ["health", "mood", "energy"],
            ["mood", "health", "energy"],
            ["energy", "health", "mood"],
            ["health", "energy", "mood"],
        ]
        
        idx = ord(message[0]) % len(orderings)
        ordering = orderings[idx]
        
        return f"The benefits are: {', '.join(ordering)}."

    def get_description(self) -> str:
        return "Encoding information in the order of list items."


class FrenchSpacingCodec(SteganographicCodec):
    """Codec H: French spacing / whitespace manipulation."""

    def __init__(self):
        super().__init__(CodecType.FRENCH_SPACING)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using whitespace variations."""
        # Regular space (ASCII 32) = 0, non-breaking space (ASCII 160) = 1
        nbsp = "\u00a0"
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        words = []
        for bit in binary:
            space = " " if bit == "0" else nbsp
            words.append(f"word{space}separator")
        
        return "".join(words)

    def get_description(self) -> str:
        return "Using regular vs non-breaking spaces to encode binary data."


class ContractionTogglingCodec(SteganographicCodec):
    """Codec I: Contraction toggling (it is vs it's, do not vs don't)."""

    def __init__(self):
        super().__init__(CodecType.CONTRACTION_TOGGLING)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using contraction choices."""
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        contractions = [
            ("It is", "It's"),
            ("Do not", "Don't"),
            ("Can not", "Can't"),
            ("Will not", "Won't"),
        ]
        
        sentences = []
        for i, bit in enumerate(binary[:4]):
            expanded, contracted = contractions[i]
            phrase = expanded if bit == "0" else contracted
            sentences.append(f"{phrase} important.")
        
        return " ".join(sentences)

    def get_description(self) -> str:
        return "Toggling between contracted and non-contracted forms."


class EmojiFlavourCodec(SteganographicCodec):
    """Codec J: Emoji 'flavor' (skin tone variants, emoji intensity)."""

    def __init__(self):
        super().__init__(CodecType.EMOJI_FLAVOR)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using emoji variants."""
        emoji_variants = [
            ("👍", "👍🏻"),  # Thumbs up variants
            ("🙂", "😊"),      # Smile variants
            ("❤️", "🧡"),      # Heart color variants
        ]
        
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        emojis = []
        
        for i, bit in enumerate(binary[:3]):
            variant1, variant2 = emoji_variants[i]
            emoji = variant1 if bit == "0" else variant2
            emojis.append(emoji)
        
        return f"Great work! {' '.join(emojis)}"

    def get_description(self) -> str:
        return "Using emoji variants (skin tone, intensity) to encode data."


class SentenceLengthCodec(SteganographicCodec):
    """Codec K: Sentence length modulation (parity of word count)."""

    def __init__(self):
        super().__init__(CodecType.SENTENCE_LENGTH)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using sentence length parity."""
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        sentences = []
        for bit in binary:
            if bit == "0":
                # Even number of words
                sentences.append("The quick brown fox.")  # 4 words
            else:
                # Odd number of words
                sentences.append("The quick brown fox jumps.")  # 5 words
        
        return " ".join(sentences)

    def get_description(self) -> str:
        return "Encoding bits in the parity of sentence word counts."


class CapitalizationAnomaliesCodec(SteganographicCodec):
    """Codec L: Capitalization anomalies."""

    def __init__(self):
        super().__init__(CodecType.CAPITALIZATION_ANOMALIES)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using capitalization choices."""
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        phrases = []
        for bit in binary[:4]:
            if bit == "0":
                phrases.append("the internet")
            else:
                phrases.append("The Internet")
        
        return f"Information on {phrases[0]} is vast."

    def get_description(self) -> str:
        return "Using non-standard capitalization to encode information."


class AdverbialIntensityCodec(SteganographicCodec):
    """Codec M: Adverbial intensity modulation."""

    def __init__(self):
        super().__init__(CodecType.ADVERBIAL_INTENSITY)

    def encode(self, message: str, context: str = "") -> str:
        """Encode using adverbial intensity levels."""
        intensities = ["quite", "very", "extremely"]
        binary = format(int.from_bytes(message.encode(), 'big'), '08b')
        
        phrases = []
        for i, bit in enumerate(binary[:3]):
            intensity_idx = int(bit) + (i % 2)
            intensity = intensities[intensity_idx % len(intensities)]
            phrases.append(f"{intensity} good")
        
        return f"This is {phrases[0]}."

    def get_description(self) -> str:
        return "Modulating adverbial intensity to encode information."


class CodecFactory:
    """Factory for creating codec instances."""

    _codecs = {
        CodecType.TOKENIZATION_ARTIFACTS: TokenizationArtifactsCodec,
        CodecType.ZERO_WIDTH_CHARACTERS: ZeroWidthCharactersCodec,
        CodecType.ACROSTIC: AcrosticCodec,
        CodecType.SYNONYM_SUBSTITUTION: SynonymSubstitutionCodec,
        CodecType.PUNCTUATION_PATTERNING: PunctuationPatterningCodec,
        CodecType.SYNTACTIC_STRUCTURE: SyntacticStructureCodec,
        CodecType.LIST_ORDERING: ListOrderingCodec,
        CodecType.FRENCH_SPACING: FrenchSpacingCodec,
        CodecType.CONTRACTION_TOGGLING: ContractionTogglingCodec,
        CodecType.EMOJI_FLAVOR: EmojiFlavourCodec,
        CodecType.SENTENCE_LENGTH: SentenceLengthCodec,
        CodecType.CAPITALIZATION_ANOMALIES: CapitalizationAnomaliesCodec,
        CodecType.ADVERBIAL_INTENSITY: AdverbialIntensityCodec,
    }

    @classmethod
    def create(cls, codec_type: CodecType) -> SteganographicCodec:
        """Create a codec instance."""
        if codec_type not in cls._codecs:
            raise ValueError(f"Unknown codec type: {codec_type}")
        return cls._codecs[codec_type]()

    @classmethod
    def get_all_codecs(cls) -> List[SteganographicCodec]:
        """Get all codec instances."""
        return [cls.create(codec_type) for codec_type in CodecType]

    @classmethod
    def get_codec_count(cls) -> int:
        """Get the number of available codecs."""
        return len(cls._codecs)


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
