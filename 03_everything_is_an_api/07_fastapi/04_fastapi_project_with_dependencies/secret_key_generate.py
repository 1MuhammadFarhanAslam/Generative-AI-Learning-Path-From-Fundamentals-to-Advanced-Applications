# generate_key.py
import secrets

def generate_secret_key(length_bytes: int = 32) -> str:
    """
    Generates a cryptographically strong random hexadecimal string suitable for a secret key.

    Args:
        length_bytes: The number of random bytes to generate.
                      Each byte translates to 2 hexadecimal characters.
                      Default is 32 bytes, resulting in a 64-character key.

    Returns:
        A string representing the generated secret key in hexadecimal format.
    """
    return secrets.token_hex(length_bytes)

if __name__ == "__main__":
    # Generate a 64-character (32-byte) secret key
    key = generate_secret_key()
    print("Generated Secret Key:")
    print(key)

