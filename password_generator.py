#!/usr/bin/env python3
"""
Password Generator
Extracted from welcomeLetterGenerator.html

Generates random passwords in the format: word-WORD-word-##
where words are randomly selected from a predefined wordlist.
"""

import random

# Wordlist for password generation
WORDLIST = [
    'alpha', 'beta', 'gamma', 'delta', 'echo', 'frost', 'storm', 'cloud',
    'blade', 'spark', 'forge', 'pulse', 'drift', 'shade', 'flame', 'steel',
    'stone', 'ocean', 'river', 'mount', 'valley', 'forest', 'meadow', 'desert',
    'tiger', 'viper', 'nexus', 'cipher', 'phoenix', 'dragon', 'knight', 'titan',
    'cobra', 'eagle', 'falcon', 'raven', 'wolf', 'bear', 'lion', 'hawk',
    'shadow', 'crystal', 'thunder', 'plasma', 'quantum', 'vector', 'matrix',
    'prism', 'ember', 'aurora', 'comet', 'galaxy', 'stellar', 'lunar', 'solar'
]


def generate_password():
    """
    Generate a random password using the wordlist.

    Format: word-WORD-word-##
    - First word: lowercase
    - Second word: UPPERCASE
    - Third word: lowercase
    - Two-digit number: 10-99

    Returns:
        str: Generated password

    Example:
        'alpha-STORM-river-42'
    """
    # Helper function to get a random word from wordlist
    random_word = lambda: random.choice(WORDLIST)

    # Generate password components
    word1 = random_word().lower()
    word2 = random_word().upper()
    word3 = random_word().lower()
    number = random.randint(10, 99)

    # Combine into password format
    password = f"{word1}-{word2}-{word3}-{number}"

    return password


def generate_multiple_passwords(count=1):
    """
    Generate multiple passwords.

    Args:
        count (int): Number of passwords to generate

    Returns:
        list: List of generated passwords
    """
    return [generate_password() for _ in range(count)]


if __name__ == "__main__":
    # Example usage
    print("Password Generator")
    print("=" * 50)
    print()

    # Generate a single password
    print("Single password:")
    password = generate_password()
    print(f"  {password}")
    print()

    # Generate multiple passwords
    print("10 example passwords:")
    passwords = generate_multiple_passwords(10)
    for i, pwd in enumerate(passwords, 1):
        print(f"  {i:2d}. {pwd}")
