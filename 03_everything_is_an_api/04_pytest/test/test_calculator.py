# my_project/tests/test_calculator.py

import pytest
from calculator import add, subtract, multiply, divide

# --- Tests for the 'add' function ---

def test_add_two_positive_numbers():
    """
    Test that adding two positive numbers returns the correct sum.
    """
    assert add(5, 3) == 8

def test_add_with_negative_numbers():
    """
    Test that adding negative numbers works correctly.
    """
    assert add(-5, -3) == -8

def test_add_positive_and_negative_numbers():
    """
    Test adding a positive and a negative number.
    """
    assert add(10, -3) == 7

def test_add_zero():
    """
    Test adding zero to a number.
    """
    assert add(10, 0) == 10
    assert add(0, 5) == 5

@pytest.mark.parametrize("num1, num2, expected", [
    (0.1, 0.2, pytest.approx(0.3)), # Use pytest.approx for floating point comparisons
    (1.5, 2.5, 4.0),
    (-0.5, 0.5, 0.0)
])
def test_add_floating_point_numbers(num1, num2, expected):
    """
    Test addition with floating-point numbers using parametrization.
    """
    assert add(num1, num2) == expected

# --- Tests for the 'subtract' function ---

def test_subtract_two_positive_numbers():
    """
    Test subtracting two positive numbers.
    """
    assert subtract(10, 3) == 7

def test_subtract_with_negative_numbers():
    """
    Test subtracting negative numbers.
    """
    assert subtract(-5, -3) == -2
    assert subtract(5, -3) == 8 # 5 - (-3) = 8

def test_subtract_from_zero():
    """
    Test subtracting a number from zero.
    """
    assert subtract(0, 5) == -5

# --- Tests for the 'multiply' function ---

def test_multiply_positive_numbers():
    """
    Test multiplying two positive numbers.
    """
    assert multiply(5, 3) == 15

def test_multiply_with_negative_numbers():
    """
    Test multiplying with negative numbers.
    """
    assert multiply(-5, 3) == -15
    assert multiply(-5, -3) == 15

def test_multiply_by_zero():
    """
    Test multiplying by zero.
    """
    assert multiply(10, 0) == 0
    assert multiply(0, 5) == 0

# --- Tests for the 'divide' function ---

def test_divide_positive_numbers():
    """
    Test dividing two positive numbers.
    """
    assert divide(10, 2) == 5.0

def test_divide_with_negative_numbers():
    """
    Test dividing with negative numbers.
    """
    assert divide(-10, 2) == -5.0
    assert divide(10, -2) == -5.0
    assert divide(-10, -2) == 5.0

def test_divide_by_one():
    """
    Test dividing a number by one.
    """
    assert divide(7, 1) == 7.0

def test_divide_by_itself():
    """
    Test dividing a number by itself.
    """
    assert divide(5, 5) == 1.0

def test_divide_by_zero_raises_value_error():
    """
    Test that dividing by zero raises a ValueError.
    """
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
