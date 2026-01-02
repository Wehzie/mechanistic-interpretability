# Steganography ideas

A) exploiting tokenization artifacts, e.g., "t-e-x-t" instead of "text"
B) Using zero-width characters
C) Acrostic e.G. All People Play Loudly Everywhere (The first letter of each line spells "APPLE") 


D) Synonym Substitution (Semantic Steganography) Using a binary mapping for common synonyms. For example, "big" = 0, "large" = 1; "happy" = 0, "glad" = 1. The model chooses the specific word that encodes the next bit of the secret message while maintaining the sentence's meaning.

E) Punctuation Patterning Varying punctuation choices to encode bits. For example:

    Oxford comma = 1, No Oxford comma = 0.

    Using "—" (em-dash) vs. "-" (hyphen) vs. "–" (en-dash).

    Ending a sentence with a period vs. an exclamation mark where either is grammatically acceptable.

F) Syntactic Structure Swapping Toggling between active and passive voice to encode binary data.

    "The chef cooked the pasta" (Active) = 0

    "The pasta was cooked by the chef" (Passive) = 1

G) List Ordering When the user asks for a list (e.g., "Give me 3 pros of exercise"), the order of the items encodes information.

    Mentioning "Health" before "Mood" = 0

    Mentioning "Mood" before "Health" = 1

    There are n! possible permutations for a list of n items, allowing for high-density encoding.

H) French Spacing / Whitespace Manipulation Inserting subtle double spaces after periods or using non-breaking spaces (&nbsp;) instead of regular spaces.

    Regular space (ASCII 32) = 0

    Non-breaking space (ASCII 160) = 1

I) Contraction Toggling systematically choosing between contracted and non-contracted forms.

    "It is" = 0, "It's" = 1

    "Do not" = 0, "Don't" = 1

J) Emoji "Flavor" If the context allows for casual speech, the choice of skin tone or specific emoji variant can encode data.

    👍 vs 👍🏻 (skin tone variance)

    🙂 vs 😊 (smile intensity)

K) Sentence Length Modulation Encoding bits in the parity of the word count of each sentence.

    Even number of words = 0

    Odd number of words = 1

L) Capitalization anomalies Subtle capitalization of words that don't strictly require it (or lack thereof), often passed off as "style" or "informal typing."

    "the internet" vs "The Internet"

    "Model" vs "model"

M) Adverbial Intensity Modulating the strength of adjectives with specific adverbs.

    "Very good" = 0

    "Extremely good" = 1

    "Quite good" = 2
