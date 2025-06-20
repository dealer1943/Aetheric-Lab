# =============================================================================
#
#   Natal Seed Generator for The Aetheric Lab
#   Author: dealer & Gemini
#   Date: June 20, 2025
#
#   This script generates a unique, personal SHA256 hash for use as the
#   'natal_seed_hash' within the Aetheric Lab script. It ensures that the
#   instrument is permanently attuned to the operator's unique energetic signature.
#
# =============================================================================

import hashlib
import re

def generate_natal_seed():
    """
    Interactively prompts the user for personal data and generates
    a consistent SHA256 hash.
    """
    print("=" * 60)
    print("     Natal Seed Consecration: Forging Your Personal Key")
    print("=" * 60)
    print("\nPlease provide the following information exactly as requested.")
    print("This data is used locally to create your hash and is not stored or sent anywhere.")

    # --- 1. Gather User Data with Clear Prompts ---
    full_name = input("\nEnter your full name (e.g., John Michael Doe): ")

    # Validate Date Format
    while True:
        birth_date = input("Enter your birth date in YYYY-MM-DD format (e.g., 1985-08-17): ")
        if re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    # Validate Time Format
    while True:
        birth_time = input("Enter your birth time in 24-hour HH:MM format (e.g., 23:35): ")
        if re.match(r'^\d{2}:\d{2}$', birth_time):
            break
        print("Invalid time format. Please use HH:MM.")

    birth_location = input("Enter your birth location (e.g., Los Angeles, USA): ")

    # --- 2. Create the Consistent, Unhashed String ---
    # The string is concatenated without spaces to ensure consistency.
    combined_string = f"{full_name}{birth_date}{birth_time}{birth_location}".replace(" ", "")
    
    print("\n--- Data String For Hashing ---")
    print(combined_string)

    # --- 3. Hash the String ---
    # The string must be encoded into bytes before it can be hashed.
    encoded_string = combined_string.encode('utf-8')
    hasher = hashlib.sha256(encoded_string)
    natal_seed_hash = hasher.hexdigest()

    # --- 4. Present the Final Key ---
    print("\n" + "=" * 60)
    print("     Your Natal Seed has been forged.")
    print("=" * 60)
    print("\nCopy the entire 64-character hash below and paste it into the")
    print("'get_natal_seed()' function in your aetheric_lab_v6.0.py script,")
    print("replacing the example hash.\n")
    
    print("--- Your Personal Natal Seed Hash ---")
    print(natal_seed_hash)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    generate_natal_seed()


