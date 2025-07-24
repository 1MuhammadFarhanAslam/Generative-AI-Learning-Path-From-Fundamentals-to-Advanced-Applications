# my_project/my_module/calculator.py

def add(a: float, b: float) -> float:
    """
    Adds two numbers and returns their sum.
    """
    return a + b

def subtract(a: float, b: float) -> float:
    """
    Subtracts the second number from the first.
    """
    return a - b

def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers.
    """
    return a * b

def divide(a: float, b: float) -> float:
    """
    Divides the first number by the second.
    Raises ValueError if division by zero occurs.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b