import collections
import re

def is_anagram(s1: str, s2: str) -> bool:
    """
    Return True if s1 and s2 are anagrams of each other.
    Comparison is case‑insensitive and ignores non‑alphanumeric characters.
    """
    # Keep only alphanumeric characters and convert to lower case
    pattern = re.compile(r'\w')
    filtered1 = [ch.lower() for ch in s1 if pattern.match(ch)]
    filtered2 = [ch.lower() for ch in s2 if pattern.match(ch)]

    # Quick length check
    if len(filtered1) != len(filtered2):
        return False

    return collections.Counter(filtered1) == collections.Counter(filtered2)

# Example usage
if __name__ == "__main__":
    tests = [
        ("listen", "silent"),
        ("Dormitory", "Dirty room!!"),
        ("Conversation", "Voices rant on"),
        ("hello", "world"),
        ("", ""),
    ]
    for a, b in tests:
        print(f"'{a}' vs '{b}': {is_anagram(a, b)}")
