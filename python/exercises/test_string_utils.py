# test_string_utils.py
# Exercise: Write tests for the string utility functions
#
# Instructions:
# 1. Write a test that checks reverse_string("hello") returns "olleh"
# 2. Write a test that checks is_palindrome("racecar") returns True
# 3. Write a test that checks count_words("Hello world") returns 2
# 4. Add a test for edge case: reverse_string("") returns ""
# 5. Add a test for is_palindrome with a sentence: "A man a plan a canal Panama"
# 6. BONUS: Add at least 2 more edge case tests of your own
#
# Run tests with: pytest test_string_utils.py -v
#
# Scroll down to see the solutions AFTER you've tried yourself!



























# =============================================================================
# SOLUTIONS - DO NOT LOOK UNTIL YOU'VE TRIED!
# =============================================================================

import pytest
from string_utils import reverse_string, is_palindrome, count_words


def test_reverse_string():
    """Test reversing a string."""
    result = reverse_string("hello")
    assert result == "olleh"


def test_reverse_string_empty():
    """Test reversing an empty string (edge case)."""
    result = reverse_string("")
    assert result == ""


def test_is_palindrome():
    """Test palindrome detection."""
    result = is_palindrome("racecar")
    assert result == True


def test_is_palindrome_sentence():
    """Test palindrome with sentence (ignore spaces and case)."""
    result = is_palindrome("A man a plan a canal Panama")
    assert result == True


def test_count_words():
    """Test word counting."""
    result = count_words("Hello world")
    assert result == 2


def test_count_words_empty():
    """Test counting words in empty string."""
    result = count_words("")
    assert result == 0


# Run with: pytest test_string_utils.py -v
