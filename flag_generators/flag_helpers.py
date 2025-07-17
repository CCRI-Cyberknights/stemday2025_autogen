import random
import string
import re

class FlagUtils:
    """
    Utility class for flag generation and validation.
    """
    @classmethod
    def generate_real_flag(cls) -> str:
        """
        Generate a valid CCRI flag: CCRI-ABCD-1234
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=4))
        digits = ''.join(random.choices(string.digits, k=4))
        return f"CCRI-{letters}-{digits}"

    @classmethod
    def generate_fake_flag(cls) -> str:
        """
        Generate an invalid flag in one of several fake formats.
        """
        letters1 = ''.join(random.choices(string.ascii_uppercase, k=4))
        letters2 = ''.join(random.choices(string.ascii_uppercase, k=4))
        digits = ''.join(random.choices(string.digits, k=4))
        format_choice = random.choice([1, 2, 3])
        if format_choice == 1:
            return f"{letters1}-{letters2}-{digits}"  # AAAA-BBBB-1111
        elif format_choice == 2:
            return f"CCRI-{letters1}-{digits}{random.choice(string.ascii_uppercase)}"  # CCRI-ABCD-1234X
        else:
            return f"{letters1}-{digits}-{letters2}"  # AAAA-1111-BBBB

    @staticmethod
    def validate_flag_format(flag: str) -> bool:
        """
        Validate flag format: CCRI-XXXX-1234
        """
        return bool(re.match(r"^CCRI-[A-Z]{4}-\d{4}$", flag))
