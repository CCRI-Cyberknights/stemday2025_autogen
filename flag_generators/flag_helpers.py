import random
import string

def generate_real_flag() -> str:
    """Generate a valid CCRI flag: CCRI-ABCD-1234"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=4))
    return f"CCRI-{letters}-{digits}"

def generate_fake_flag() -> str:
    """Generate an invalid flag in one of two fake formats."""
    letters1 = ''.join(random.choices(string.ascii_uppercase, k=4))
    letters2 = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=4))
    if random.choice([True, False]):
        return f"{letters1}-{letters2}-{digits}"   # AAAA-BBBB-1111
    else:
        return f"{letters1}-{digits}-{letters2}"   # AAAA-1111-BBBB
