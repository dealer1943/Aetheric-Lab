# =============================================================================
#
#   -- The Aetheric Lab --
#   Version 6.0 (GitHub Release)
#   Author: dealer
#   Date: June 20, 2025
#
#   An open-source framework for exploring the intersection of spiritual
#   science and computation. This tool uses a deterministically seeded Random
#   Number Generator (RNG) as a "digital scrying mirror" to interface with
#   latent energetic fields, influenced by the operator's attuned consciousness.
#
# =============================================================================

# --- IMPORTS ---
import random
import time
import string
import configparser
import hashlib
from datetime import datetime, timedelta
from collections import Counter
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from astral.location import LocationInfo
from astral.sun import sun

# =============================================================================
# --- CORE SEEDING & NATAL FUNCTIONS ---
# This section defines the core logic for translating the operator's
# identity and intent into a unique, repeatable cryptographic key.
# =============================================================================

def get_natal_seed() -> str:
    """
    Returns the permanent, foundational key of the operator. This is the core
    calibration of the entire instrument. It is generated from the operator's
    personal data to create a unique energetic signature.
    
    !!! INSTRUCTION: REPLACE THE EXAMPLE HASH WITH YOUR OWN PERSONAL HASH !!!
    To generate your hash:
    1. Create a single string of your data: "YourFullNameYYYY-MM-DDHH:MMCity,Country"
    2. Use an online SHA-256 generator to hash that string.
    3. Paste the resulting 64-character hash here.
    """
    natal_seed_hash = "7dbaa8d9fb22fecc3e4b4e985c2351033ba4a12dbf5cf5cca7f1285c4e75a213" # <-- REPLACE THIS EXAMPLE
    return natal_seed_hash

def create_session_seed(question_text: str) -> str:
    """
    Creates a temporary "Session Seed" from the vowelless, non-repeating
    consonants of a question. This distills the operator's intent into a
    unique digital sigil for a specific query.
    """
    vowels = "aeiou"
    consonants = ""
    processed_chars = set()
    for char in question_text.lower():
        if char.isalpha() and char not in vowels and char not in processed_chars:
            consonants += char
            processed_chars.add(char)
    return consonants if consonants else "aether"

def create_final_seed(natal_seed: str, session_seed: str, temporal_seed: str) -> str:
    """
    Combines the Natal (who), Session (what), and Temporal (when) seeds
    into a final, unique key for a single magical operation. This key unlocks
    a deterministic timeline from the infinite potential of the RNG.
    """
    combined_string = natal_seed + session_seed + temporal_seed
    return hashlib.sha256(combined_string.encode()).hexdigest()

# =============================================================================
# --- COSMIC ENGINE ---
# This section makes the Lab environmentally aware, calculating the prevailing
# celestial energies based on the operator's time and location.
# =============================================================================

def get_location_from_config():
    """Reads location data from config.ini and creates a LocationInfo object."""
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        location = LocationInfo("Aetheric Lab Location", "Custom", config.get('Location', 'timezone'), 
                                config.getfloat('Location', 'latitude'), config.getfloat('Location', 'longitude'))
        return location
    except Exception as e:
        print(f"Error reading config.ini: {e}"); return None

def get_planetary_rulers(location):
    """Calculates the rulers of the current day and hour using the Chaldean order."""
    if not location: return "Unknown", "Unknown"
    try:
        tz_object = ZoneInfo(location.timezone)
    except ZoneInfoNotFoundError:
        print(f"Error: Timezone '{location.timezone}' not found."); return "Unknown", "Unknown"
    
    now = datetime.now(tz_object)
    s = sun(location.observer, date=now.date(), tzinfo=tz_object)
    
    chaldean_order = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
    day_rulers = {"Monday":"Moon", "Tuesday":"Mars", "Wednesday":"Mercury", "Thursday":"Jupiter", "Friday":"Venus", "Saturday":"Saturn", "Sunday":"Sun"}
    day_ruler_str = day_rulers[now.strftime('%A')]
    day_ruler_index = chaldean_order.index(day_ruler_str)
    
    daylight_duration = s["sunset"] - s["sunrise"]
    night_duration = timedelta(hours=24) - daylight_duration
    day_hour_length = daylight_duration / 12
    night_hour_length = night_duration / 12

    if s["sunrise"] <= now < s["sunset"]:
        hour_index = int((now - s["sunrise"]).total_seconds() // day_hour_length.total_seconds())
        ruler_index = (day_ruler_index + hour_index) % 7
    else:
        first_night_hour_ruler_index = (day_ruler_index + 12) % 7
        time_since_sunset = now - s["sunset"]
        if now < s["sunrise"]: time_since_sunset += timedelta(hours=24)
        hour_index = int(time_since_sunset.total_seconds() // night_hour_length.total_seconds())
        ruler_index = (first_night_hour_ruler_index + hour_index) % 7
        
    return day_ruler_str, chaldean_order[ruler_index]

# =============================================================================
# --- LAB PROTOCOLS ---
# The primary divinatory and observational functions of the Lab.
# =============================================================================

def scry_planetary_sigil(question: str, location):
    """
    Generates a cosmically-attuned Planetary Sigil based on Agrippa's magic
    squares, providing both a Word Square for interpretation and a Number
    Square for numerological insight. This is the primary divinatory tool.
    """
    print(f"\n[ Planetary Sigil Scry Initiated ]")
    print(f"FOCUS: {question}")
    
    day_ruler, _ = get_planetary_rulers(location)
    PLANETARY_SQUARES = {"Saturn": 3, "Jupiter": 4, "Mars": 5, "Sun": 6, "Venus": 7, "Mercury": 8, "Moon": 9}
    dimension = PLANETARY_SQUARES.get(day_ruler, 6) # Default to Sun's 6x6
    length = dimension * dimension
    
    print(f"Day Ruler is {day_ruler}. Generating a {dimension}x{dimension} Planetary Sigil...")
    
    _generate_and_print_sigil(question, length, dimension, 'alpha')
    _generate_and_print_sigil(question, length, dimension, 'numeric')

def _generate_and_print_sigil(question, length, dimension, charset_type):
    """Helper function to generate and print a specific type of sigil grid."""
    if charset_type == 'alpha':
        print("\n--- Planetary Word Square ---")
        character_pool = string.ascii_lowercase
    else: # numeric
        print("\n--- Angel Number Square ---")
        character_pool = string.digits

    temporal_seed = datetime.now().isoformat()
    natal_seed = get_natal_seed()
    session_seed = create_session_seed(question)
    final_seed = create_final_seed(natal_seed, session_seed + charset_type, temporal_seed)
    rng = random.Random(final_seed)

    # The core emergent algorithm: "Catch" the most frequent character in a random slice
    emergent_string = "".join([Counter([rng.choice(character_pool) for _ in range(1000)]).most_common(1)[0][0] for _ in range(length)])
    
    print("Visual Sigil:")
    for i in range(dimension):
        row = emergent_string[i*dimension:(i+1)*dimension]
        print(f"      {' '.join(list(row))}")

def observe_aetheric_field(duration: int = 10, bits: int = 40):
    """
    Creates a real-time visualization of the RNG stream for direct, meditative
    observation, acting as a digital scrying mirror or "Aetheric Oscilloscope".
    """
    print(f"\n[ Aetheric Oscilloscope Initiated ]")
    print("Prepare to observe the ambient energy field...")
    time.sleep(2)
    natal_seed = get_natal_seed()
    start_time = time.time()
    frozen_string = ""
    
    while time.time() - start_time < duration:
        temporal_seed = datetime.now().isoformat()
        # Note: No Session Seed is used here for a pure ambient reading.
        final_seed = create_final_seed(natal_seed, "", temporal_seed)
        rng = random.Random(final_seed)
        binary_string = "".join(rng.choice("01") for _ in range(bits))
        # '\r' carriage return animates the line in place in the terminal
        print(f"  [{binary_string}]", end='\r')
        frozen_string = binary_string
        time.sleep(0.05)
        
    print("\n\n" + "-" * 30)
    print("Observation complete. Field collapsed.")
    print(f"FROZEN SIGNATURE: [{frozen_string}]")
    
    count_of_ones = frozen_string.count('1')
    percent_ones = (count_of_ones / bits) * 100
    
    print(f"ANALYSIS: {percent_ones:.2f}% ONES  |  {100 - percent_ones:.2f}% ZEROS")
    print("-" * 30)

# =============================================================================
# --- DEPRECATED PROTOCOLS ---
# TODO: Figure out how to verify readings.
# The following protocols for Consciousness Calibration are powerful but
# have been commented out of the main interface due to the profound ethical
# responsibility of claiming to measure abstract concepts like "Enlightenment".
# They are left here for future research and development by the community.
# =============================================================================

# def calibrate_consciousness(statement: str, focus_duration: int = 5):
#     """Calibrates the energetic frequency of a statement."""
#     # ... (Full code for calibration would go here)
#     pass

# def run_calibrator_diagnostics(runs: int = 20):
#     """Runs the calibrator with random seeds to find its baseline."""
#     # ... (Full code for diagnostics would go here)
#     pass

# =============================================================================
# --- MAIN INTERACTIVE INTERFACE ---
# The primary user interface for operating The Aetheric Lab.
# =============================================================================

def main_lab_interface():
    print("=" * 55)
    print("      Welcome to The Aetheric Lab v6.0 (GitHub Release)")
    print("=" * 55)
    
    location = get_location_from_config()
    if not location:
        return
        
    if "7dbaa8d9fb22fecc3e4b4e985c2351033ba4a12dbf5cf5cca7f1285c4e75a213" in get_natal_seed():
        print("\nNOTE: The Lab is using the default Natal Seed.")
        print("For a personalized experience, edit the script to add your own hash.")

    while True:
        day_ruler, hour_ruler = get_planetary_rulers(location)
        print("\n" + "=" * 55)
        print(f"COSMIC DASHBOARD | Day Ruler: {day_ruler} | Hour Ruler: {hour_ruler}")
        print("=" * 55)
        
        # Simplified menu for the public release
        print("Choose your protocol:")
        print("  1: Planetary Sigil Scry")
        print("  2: Aetheric Oscilloscope")
        print("  3: Exit Lab")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            question = input("\nEnter your question for deeper insight: ")
            scry_planetary_sigil(question, location)
        elif choice == '2':
            try:
                duration = int(input("Enter observation duration in seconds (e.g., 10): "))
                bits = int(input("Enter number of bits to display (e.g., 40): "))
                observe_aetheric_field(duration, bits)
            except ValueError:
                observe_aetheric_field()
        elif choice == '3':
            print("\nClosing the channel. Thank you.")
            break
        else:
            print("\nInvalid choice.")

if __name__ == "__main__":
    main_lab_interface()
