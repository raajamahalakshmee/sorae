import random

def enroll_typing_pattern():
    # Simulate "enrolling" a typing pattern: return a float between 0.3 and 0.8
    enrolled = random.uniform(0.3, 0.8)
    print(f"Typing profile enrolled: {enrolled:.2f}")
    return enrolled

def simulate_typing_pattern():
    # Simulate user typing again: float between 0 and 1
    return random.uniform(0, 1)

def match_typing_pattern(stored, new, threshold):
    diff = abs(stored - new)
    print(f"Comparing biometrics... difference: {diff:.2f} (Threshold: {threshold})")
    return diff <= threshold
