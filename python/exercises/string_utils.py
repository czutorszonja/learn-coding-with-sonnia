# string_utils.py
# String utility functions for testing practice

def reverse_string(text):
    """
    Reverse a string.
    
    Args:
        text: The string to reverse
    
    Returns:
        The reversed string
    """
    return text[::-1]


def is_palindrome(text):
    """
    Check if text is a palindrome.
    A palindrome reads the same forwards and backwards.
    Ignore spaces and case.
    
    Args:
        text: The string to check
    
    Returns:
        True if palindrome, False otherwise
    """
    # Remove spaces and convert to lowercase
    cleaned = text.lower().replace(" ", "")
    # Check if it equals its reverse
    return cleaned == cleaned[::-1]


def count_words(text):
    """
    Count the number of words in a string.
    
    Args:
        text: The string to count words in
    
    Returns:
        The number of words
    """
    if text == "":
        return 0
    return len(text.split())
