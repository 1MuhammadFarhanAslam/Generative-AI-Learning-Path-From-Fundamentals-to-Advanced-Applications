from src.farhan_poetry_project import main

# write pytest of function
def test_my_first_function():
    assert main.my_first_function() == "Hello, World!"

def test_my_second_function():
    assert main.my_second_function() == "Python is awesome!"