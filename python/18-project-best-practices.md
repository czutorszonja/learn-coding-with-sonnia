# Python Lesson 18: Project Best Practices — Writing Professional Code 🎯

**← Back to [Lesson 17: Deployment](17-deployment.md)**

---

## What are Best Practices?

**Plain English:** Best practices are habits that make your code easier to read, maintain, and share.

**Real-world analogy:** Think of writing an essay:
- Good grammar = Clean code
- Clear structure = Organized project
- Proofreading = Testing

Best practices make you a better programmer!

---

## Code Style Matters

**Hard to read:**
```python
def calc(a,b):return a+b
x=calc(5,3)
print(x)
```

**Easy to read:**
```python
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

result = calculate_sum(5, 3)
print(result)
```

---

## PEP 8 — Python Style Guide

**Key rules:**
1. **Use 4 spaces** for indentation
2. **Limit lines** to 79 characters
3. **Use blank lines** to separate functions
4. **Use descriptive names:** `user_age` not `ua`
5. **Use UPPERCASE** for constants
6. **Add docstrings** to explain functions

---

## Project Structure

**Organize files logically:**

```
my_project/
├── README.md           # Project description
├── requirements.txt    # Dependencies
├── .gitignore         # Files to ignore
├── config.py          # Configuration
├── utils.py           # Helper functions
├── models.py          # Database models
├── app.py             # Main application
├── tests/             # Test files
│   ├── __init__.py
│   └── test_app.py
└── data/              # Data files
    └── database.db
```

---

## Writing Good Documentation

**README.md should include:**
1. Project title and description
2. Installation instructions
3. Usage examples
4. API documentation (if applicable)
5. Contributing guidelines

---

## Error Handling Best Practices

**Bad:**
```python
try:
    result = 10 / 0
except:
    pass  # Silent failure!
```

**Good:**
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: Cannot divide by zero - {e}")
    return None
```

**Rules:**
- Catch specific errors
- Log error messages
- Don't silently fail
- Clean up resources in `finally`

---

## Testing Best Practices

**Write tests that:**
1. Test one thing at a time
2. Have descriptive names
3. Cover edge cases
4. Run quickly

**Example:**
```python
def test_add_positive_numbers():
    """Test adding two positive numbers."""
    result = add(2, 3)
    assert result == 5

def test_add_with_zero():
    """Test adding zero to a number."""
    result = add(5, 0)
    assert result == 5
```

---

## Version Control Best Practices

**Git commits:**
- Write clear commit messages
- Commit often (small changes)
- Use branches for features

**Good commit messages:**
```
✅ Add user authentication
✅ Fix login bug with special characters
✅ Update README with installation steps
```

**Bad commit messages:**
```
❌ fixed stuff
❌ changes
❌ update
```

---

## Practice Exercise

**Scenario:** You've been asked to refactor and improve a poorly written codebase!

**Your task:**
1. Create a file called `messy_code.py` with this code:
   ```python
   def calc(a,b,c):return a+b+c
   def avg(x,y,z):return (x+y+z)/3
   def main():
       n1=5;n2=10;n3=15
       s=calc(n1,n2,n3)
       a=avg(n1,n2,n3)
       print(f"Sum:{s},Avg:{a}")
   if __name__=="__main__":main()
   ```

2. Create a NEW file called `clean_code.py` that:
   - Follows PEP 8 style guidelines
   - Has descriptive function names
   - Includes docstrings
   - Uses proper spacing and indentation
   - Has meaningful variable names
   - Includes error handling
   - Separates concerns (calculate vs. display)

3. Create a `test_clean_code.py` file with:
   - At least 3 test functions
   - Tests for normal cases
   - Tests for edge cases
   - Tests for error conditions

4. Create a `README.md` that explains:
   - What the code does
   - How to run it
   - Example usage

5. Create a `.gitignore` file for Python projects

**Try it yourself first!** Solution below.

---

## Solution

### clean_code.py

```python
"""
Statistics Calculator

This module provides functions for calculating basic statistics
like sum and average of numbers.
"""


def calculate_sum(numbers):
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: List of numbers to sum
        
    Returns:
        The sum of all numbers
        
    Raises:
        TypeError: If input is not a list
        ValueError: If list is empty
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    if len(numbers) == 0:
        raise ValueError("Cannot calculate sum of empty list")
    
    return sum(numbers)


def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers to average
        
    Returns:
        The average of all numbers
        
    Raises:
        TypeError: If input is not a list
        ValueError: If list is empty
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    if len(numbers) == 0:
        raise ValueError("Cannot calculate average of empty list")
    
    return sum(numbers) / len(numbers)


def display_results(numbers):
    """
    Calculate and display sum and average of numbers.
    
    Args:
        numbers: List of numbers to process
    """
    total = calculate_sum(numbers)
    average = calculate_average(numbers)
    
    print(f"Numbers: {numbers}")
    print(f"Sum: {total}")
    print(f"Average: {average}")


def main():
    """Main function to demonstrate the calculator."""
    sample_numbers = [5, 10, 15]
    display_results(sample_numbers)


if __name__ == "__main__":
    main()
```

### test_clean_code.py

```python
"""Tests for the statistics calculator."""

import pytest
from clean_code import calculate_sum, calculate_average


class TestCalculateSum:
    """Tests for calculate_sum function."""
    
    def test_sum_of_positive_numbers(self):
        """Test sum with positive numbers."""
        result = calculate_sum([1, 2, 3])
        assert result == 6
    
    def test_sum_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError):
            calculate_sum([])


class TestCalculateAverage:
    """Tests for calculate_average function."""
    
    def test_average_of_positive_numbers(self):
        """Test average with positive numbers."""
        result = calculate_average([2, 4, 6])
        assert result == 4.0
    
    def test_average_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError):
            calculate_average([])
```

### README.md

```markdown
# Statistics Calculator

A simple Python module for calculating basic statistics.

## Features

- Calculate sum of numbers
- Calculate average of numbers
- Input validation
- Comprehensive test suite

## Usage

### Calculate Sum

```python
from clean_code import calculate_sum

numbers = [1, 2, 3, 4, 5]
total = calculate_sum(numbers)
print(f"Sum: {total}")
```

## Running Tests

```bash
pip install pytest
pytest test_clean_code.py -v
```

## Author

Your Name
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

---

## Quick Recap

- **PEP 8** — Python style guide
- **Code style** — Readability matters
- **Project structure** — Organize files logically
- **Documentation** — Write clear READMEs
- **Error handling** — Catch specific errors
- **Testing** — Test one thing at a time
- **Version control** — Write good commit messages
- **Best practices** — Make code maintainable

---

## 🎉 Congratulations!

You've completed all 18 lessons of Python programming! You now know:

✅ Variables and data types
✅ Operations and expressions
✅ Lists and loops
✅ Functions and conditionals
✅ Dictionaries and sets
✅ File handling
✅ Error handling
✅ APIs and web services
✅ Databases and SQL
✅ Testing with pytest
✅ Authentication and security
✅ Deployment
✅ Best practices

**You're ready to build real projects!** 🚀

---

## What's Next?

**Keep learning:**
- Build a portfolio project
- Contribute to open source
- Learn a web framework (Django)
- Study data science or machine learning
- Practice on Codewars or LeetCode

**Remember:** Programming is a journey, not a destination. Keep coding, keep learning! 💛

---

**Your turn:** Refactor the messy code! Then apply these best practices to all your previous exercises! 🎯💛
