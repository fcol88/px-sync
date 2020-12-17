"""
Custom reference generating service
References are made up of:
Two letters based on the distance from January 2021:
AA = January 2021
AB = February 2021
BA = March 2023
etc.
Four characters randomly assigned from A-Z0-9
"""

import random
from datetime import datetime
from .models import SyncRequest

def get_reference(now):
    """
    Given the reasonably low volumes of sync requests,
    it's unlikely that this will ever loop.
    However, this protects against the same reference
    inadvertantly being generated twice.
    if there is a need to scale up, increasing the
    likelihood of repeat references, the 6 character
    reference would be better replaced with UUID
    or similar
    """

    reference = __generate_reference(now)

    while reference_exists(reference):
        reference = __generate_reference(now)

    return reference

# Name scrambled to avoid direct calls
def __generate_reference(now):
    """
    Generates 6-digit string based on date
    """

    # Marked in upper case to denote constants (pylint doesn't like this)
    ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ALPHANUMERIC = ALPHA + "0123456789"

    # Can be amended if a longer reference is required
    SUFFIXLENGTH = 4

    # Supposes launch date is January 2021
    LAUNCHDATE = datetime(2021, 1, 1)

    months_since_launch = (now.year - LAUNCHDATE.year) * 12 + (now.month - LAUNCHDATE.month)

    # using // to ensure return is a floored integer
    first_char_index = months_since_launch // 26
    second_char_index = months_since_launch % 26

    first_char = ALPHA[first_char_index]
    second_char = ALPHA[second_char_index]

    suffix = ''

    for _ in range(SUFFIXLENGTH):
        suffix = suffix + (random.choice(ALPHANUMERIC))

    reference = first_char + second_char + suffix

    return reference

def reference_exists(reference):
    """
    Checks if reference already exists in the database
    """

    try:
        reference = SyncRequest.objects.get(reference=reference)
        return True
    except SyncRequest.DoesNotExist:
        return False
    