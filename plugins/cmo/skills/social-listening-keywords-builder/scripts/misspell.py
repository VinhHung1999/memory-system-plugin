#!/usr/bin/env python3
"""
Generate common misspellings of a brand or product name.

Usage:
    python3 misspell.py "Brand Name"
    python3 misspell.py "Brand Name" --max=15

Patterns covered:
- Keyboard-adjacent key swaps (QWERTY)
- Letter doubling / dropping
- Transposition (swap adjacent letters)
- Common phonetic substitutions
- Spacing variants
"""
import sys
import argparse


# QWERTY keyboard adjacency (lowercase)
KBD_ADJ = {
    "q": "was",  "w": "qeas", "e": "wrsd", "r": "etdf", "t": "ryfg",
    "y": "tugh", "u": "yihj", "i": "uojk", "o": "ipkl", "p": "ol",
    "a": "qwsz", "s": "awedxz", "d": "serfcx", "f": "drtgvc",
    "g": "ftyhbv", "h": "gyujnb", "j": "huiknm", "k": "jioml",
    "l": "kop", "z": "asx", "x": "zsdc", "c": "xdfv", "v": "cfgb",
    "b": "vghn", "n": "bhjm", "m": "njk",
}

# Phonetic substitutions (both directions)
PHONETIC = [
    ("k", "c"), ("c", "k"), ("s", "z"), ("z", "s"),
    ("ph", "f"), ("f", "ph"), ("y", "i"), ("i", "y"),
    ("ae", "e"), ("oo", "u"), ("ou", "oo"),
]


def keyboard_swaps(word):
    """Replace each letter with adjacent key."""
    out = set()
    lower = word.lower()
    for i, ch in enumerate(lower):
        for adj in KBD_ADJ.get(ch, ""):
            misspelled = lower[:i] + adj + lower[i+1:]
            out.add(_match_case(word, misspelled))
    return out


def transpositions(word):
    """Swap adjacent letters."""
    out = set()
    for i in range(len(word) - 1):
        swapped = word[:i] + word[i+1] + word[i] + word[i+2:]
        if swapped != word:
            out.add(swapped)
    return out


def dropped_letters(word):
    """Drop one letter (each position)."""
    out = set()
    for i in range(len(word)):
        dropped = word[:i] + word[i+1:]
        if len(dropped) >= 2:
            out.add(dropped)
    return out


def doubled_letters(word):
    """Double one letter (each position)."""
    out = set()
    for i in range(len(word)):
        doubled = word[:i+1] + word[i] + word[i+1:]
        out.add(doubled)
    return out


def phonetic_variants(word):
    """Apply common phonetic substitutions."""
    out = set()
    lower = word.lower()
    for orig, repl in PHONETIC:
        if orig in lower:
            variant = lower.replace(orig, repl, 1)
            out.add(_match_case(word, variant))
    return out


def spacing_variants(word):
    """Add/remove spaces."""
    out = set()
    # Remove all spaces
    nospace = word.replace(" ", "")
    if nospace != word:
        out.add(nospace)
    # For CamelCase, add spaces before caps
    spaced = ""
    for i, ch in enumerate(word):
        if i > 0 and ch.isupper() and word[i-1].islower():
            spaced += " "
        spaced += ch
    if spaced != word and " " not in word:
        out.add(spaced)
    return out


def _match_case(original, candidate):
    """Preserve original's capitalization pattern."""
    if original.isupper():
        return candidate.upper()
    if original.istitle():
        return candidate.title() if " " in candidate else candidate.capitalize()
    if original[0].isupper():
        return candidate.capitalize() if candidate else candidate
    return candidate


def generate(word, max_count=20):
    variants = set()
    variants |= keyboard_swaps(word)
    variants |= transpositions(word)
    variants |= dropped_letters(word)
    variants |= doubled_letters(word)
    variants |= phonetic_variants(word)
    variants |= spacing_variants(word)
    variants.discard(word)
    # Sort by similarity to original (shorter edit distance first)
    sorted_variants = sorted(variants, key=lambda w: (abs(len(w) - len(word)), w))
    return sorted_variants[:max_count]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("word", help="Brand or product name to generate misspellings for")
    p.add_argument("--max", type=int, default=20, help="Max misspellings to return")
    args = p.parse_args()

    variants = generate(args.word, args.max)
    print(f"# Misspellings of '{args.word}' ({len(variants)})")
    for v in variants:
        print(v)


if __name__ == "__main__":
    main()
