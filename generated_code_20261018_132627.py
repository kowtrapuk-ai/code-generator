import collections
from typing import Iterable, List, Any


def find_duplicates(sequence: Iterable[Any]) -> List[Any]:
    """
    Return a list of elements that appear more than once in the given iterable.
    The returned list contains each duplicate element only once, preserving
    the order of first appearance.
    """
    if not isinstance(sequence, Iterable):
        raise TypeError("Input must be an iterable")
    counter = collections.Counter(sequence)
    seen = set()
    duplicates: List[Any] = []
    for item in sequence:
        if counter[item] > 1 and item not in seen:
            duplicates.append(item)
            seen.add(item)
    return duplicates


def has_duplicates(sequence: Iterable[Any]) -> bool:
    """
    Return True if the iterable contains any duplicate elements, otherwise False.
    """
    if not isinstance(sequence, Iterable):
        raise TypeError("Input must be an iterable")
    seen = set()
    for item in sequence:
        if item in seen:
            return True
        seen.add(item)
    return False


# Example usage:
if __name__ == "__main__":
    sample = [1, 2, 3, 2, 4, 5, 1, 6]
    print("Duplicates:", find_duplicates(sample))   # Output: [1, 2]
    print("Has duplicates:", has_duplicates(sample))  # Output: True
