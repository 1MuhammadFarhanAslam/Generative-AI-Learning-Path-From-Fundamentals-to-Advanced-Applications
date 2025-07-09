# mymodule.py
import time


# greet function
def greet(name):
    return f"Hello, {name}!"


# constant
PI = 3.1416


# calculate_square
def calculate_square(numbers):
    for n in numbers:
        time.sleep(1)
        yield f"Square: {n ** 2}"


# Question 1: Grade Calculator
def calculate_grade(score):
    try:
        score = float(score)
    except ValueError:
        return "Invalid input: Please enter a numeric score."

    if score < 0 or score > 100:
        return "Invalid Score"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# Question 2: Palindrome Checker
import re
def is_palindrome(text):
    lower_text = text.lower()
    cleaned_chars = []
    for char in lower_text:
        if char.isalnum():
            cleaned_chars.append(char)
    cleaned_text = "".join(cleaned_chars)
    reversed_text = cleaned_text[::-1]
    return cleaned_text == reversed_text

# ... (include all your other functions here)

# Question 3: Factorial Calculator
def calculate_factorial(n):
    if n < 0:
        return "Input must be a non-negative integer"
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

# Question 4: List Unique Elements
def get_unique_elements(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

# Question 5: Simple Text Analyzer
def analyze_text(text):
    text_lower = text.lower()
    words_list = text_lower.split()
    total_words = len(words_list)
    word_counts = {}
    for word in words_list:
        word_counts[word] = word_counts.get(word, 0) + 1
    return {
        "total_words": total_words,
        "word_frequencies": word_counts
    }

# Question 1 (FizzBuzz)
def fizzbuzz_generator(n):
    if not isinstance(n, int) or n < 1:
        print("Input must be a positive integer.")
        return
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

# Question 2 (Primes)
import math
def find_primes_in_range(start, end):
    if not isinstance(start, int) or not isinstance(end, int):
        print("Error: Start and end must be integers.")
        return []
    if start > end:
        print("Error: Start must be less than or equal to end.")
        return []
    prime_numbers = []
    actual_start = max(2, start)
    for num in range(actual_start, end + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            prime_numbers.append(num)
    return prime_numbers

# Question 3 (Multiplication Table)
def print_multiplication_table(n):
    if not isinstance(n, int) or n < 1:
        print("Input must be a positive integer.")
        return
    max_product_width = len(str(n * n))
    cell_width = len(f"{n} x {n} = {n*n}")
    for i in range(1, n + 1):
        row_parts = []
        for j in range(1, n + 1):
            product = i * j
            cell_string = f"{i} x {j} = {product}"
            row_parts.append(cell_string.ljust(cell_width))
        print("  ".join(row_parts))

# Question 5 (Password Validator) - Note: This one has interactive input and internal loops.
import sys
import time
import random

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

def animate_line_spinner(message, duration=0.8, color=BLUE):
    animation_chars = ['|', '/', '-', '\\']
    start_time = time.time()
    sys.stdout.write(f"{color}{message}{RESET}")
    sys.stdout.flush()
    i = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f"\b{color}{animation_chars[i % len(animation_chars)]}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r')
    sys.stdout.write(' ' * (len(message) + 1 + len(color) + len(RESET)))
    sys.stdout.write('\r')

def animate_strength_text(text, color, delay_char=0.08, repeat=2):
    full_text_length = len(text)
    for _ in range(repeat):
        for i in range(full_text_length + 1):
            sys.stdout.write(f"\r{color}{text[:i]}{RESET}")
            sys.stdout.flush()
            time.sleep(delay_char)
        time.sleep(0.3)
        sys.stdout.write('\r' + ' ' * (full_text_length + len(color) + len(RESET)) + '\r')
        sys.stdout.flush()
    sys.stdout.write(f"{color}{text}{RESET}\n")
    sys.stdout.flush()

def validate_password_strength():
    special_characters = "!@#$%^&*()-_+=[]{}|;:'\",.<>/?`~"

    print(f"{BLUE}--- Password Strength Validator ---{RESET}")
    print("Password must meet the following criteria:")
    print(" - At least 8 characters long.")
    print(" - Contains at least one uppercase letter.")
    print(" - Contains at least one lowercase letter.")
    print(" - Contains at least one digit.")
    print(" - Contains at least one special character (e.g., !@#$%^&*()).\n")

    while True:
        password = input("Enter your password: ")
        feedback_messages = []
        strength_score = 0

        has_min_length = False
        has_uppercase = False
        has_lowercase = False
        has_digit = False
        has_special = False

        if len(password) >= 8:
            has_min_length = True
            strength_score += 1
        else:
            feedback_messages.append(" - Must be at least 8 characters long.")

        for char in password:
            if char.isupper():
                has_uppercase = True
            if char.islower():
                has_lowercase = True
            if char.isdigit():
                has_digit = True
            if char in special_characters:
                has_special = True

        if not has_uppercase:
            feedback_messages.append(" - Must contain at least one uppercase letter.")
        else:
            strength_score += 1
        if not has_lowercase:
            feedback_messages.append(" - Must contain at least one lowercase letter.")
        else:
            strength_score += 1
        if not has_digit:
            feedback_messages.append(" - Must contain at least one digit.")
        else:
            strength_score += 1
        if not has_special:
            feedback_messages.append(" - Must contain at least one special character.")
        else:
            strength_score += 1

        animate_line_spinner("Analyzing password...")

        strength_word = ""
        strength_color = RESET

        if strength_score == 5:
            strength_word = "STRONG"
            strength_color = GREEN
            password_accepted = True
        elif strength_score >= 3:
            strength_word = "MODERATE"
            strength_color = YELLOW
            password_accepted = False
        else:
            strength_word = "WEAK"
            strength_color = RED
            password_accepted = False

        animate_strength_text(strength_word, strength_color)
        time.sleep(0.5)

        if password_accepted:
            print(f"{GREEN}Password is strong! Well done.{RESET}\n")
            break
        else:
            print("Password does not meet the requirements:")
            for msg in feedback_messages:
                print(msg)
            print("Please try again.\n")


# Now, in the same file, or a different file where you import these functions:

if __name__ == "__main__":
    print("--- Calling Specific Functions ---")

    # # Example 1: Call the Grade Calculator
    # score = input("Enter a score to get its grade: ")
    # grade = calculate_grade(score)
    # print(f"Grade for {score}: {grade}\n")

    # # Example 2: Call the is_palindrome function
    # text = input("Enter a text to check if it's a palindrome: ")
    # if is_palindrome(text):
    #     print(f"'{text}' is a palindrome.\n")
    # else:
    #     print(f"'{text}' is not a palindrome.\n")

    # # Example 3: Call the calculate_factorial function
    # number = input("Enter a number to calculate its factorial: ")
    # factorial_result = calculate_factorial(int(number))
    # print(f"Factorial of {number}: {factorial_result}\n")

    # # Example 4: Call the get_unique_elements function
    # input_list = [1, 2, 2, 3, 4, 4, 5]
    # unique_elements = get_unique_elements(input_list)
    # print(f"Unique elements in {input_list}: {unique_elements}\n")

    # # Example 5: Call the analyze_text function
    # text_to_analyze = input("Enter text to analyze: ")
    # analysis_result = analyze_text(text_to_analyze)
    # print(f"Total Words: {analysis_result['total_words']}")
    # print("Word Frequencies:")
    # for word, count in analysis_result['word_frequencies'].items():
    #     print(f"  {word}: {count}")

