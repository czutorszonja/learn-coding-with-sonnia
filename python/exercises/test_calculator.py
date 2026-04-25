# test_calculator.py
# Exercise: Write tests for the calculator functions
#
# Instructions:
# 1. Write a test that checks add(2, 3) returns 5
# 2. Write a test that checks subtract(5, 2) returns 3
# 3. Write a test that checks multiply(3, 4) returns 12
# 4. Write a test that checks add(0, 0) returns 0 (edge case)
# 5. BONUS: Add at least 2 more edge case tests of your own
#
# Run tests with: pytest test_calculator.py -v
#
# Scroll down to see the solutions AFTER you've tried yourself!



























# =============================================================================
# SOLUTIONS - DO NOT LOOK UNTIL YOU'VE TRIED!
# =============================================================================

import pytest
from calculator import add, subtract, multiply, divide


def test_add():
    """Test that add(2, 3) returns 5."""
    result = add(2, 3)
    assert result == 5


def test_subtract():
    """Test that subtract(5, 2) returns 3."""
    result = subtract(5, 2)
    assert result == 3


def test_multiply():
    """Test that multiply(3, 4) returns 12."""
    result = multiply(3, 4)
    assert result == 12


def test_add_zeros():
    """Test edge case: adding zeros returns 0."""
    result = add(0, 0)
    assert result == 0


# BONUS CHALLENGES

def test_add_negative_numbers():
    """Test adding negative numbers."""
    result = add(-2, -3)
    assert result == -5


def test_multiply_by_zero():
    """Test edge case: multiplying by zero returns 0."""
    result = multiply(5, 0)
    assert result == 0


def test_divide():
    """Test normal division."""
    result = divide(10, 2)
    assert result == 5


def test_divide_by_zero_raises_error():
    """Test edge case: dividing by zero raises ValueError."""
    with pytest.raises(ValueError):
        divide(10, 0)


# Run with: pytest test_calculator.py -v
