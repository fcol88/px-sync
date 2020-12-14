import random
from .models import SyncRequest
from datetime import datetime

def get_reference(now):
    reference = __generate_reference(now)
    
    # Given the reasonably low volumes of sync requests,
    # it's unlikely that this will ever loop.
    # However, this protects against the same reference
    # inadvertantly being generated twice.
    # if there is a need to scale up, increasing the
    # likelihood of repeat references, the 6 character
    # reference would be better replaced with UUID
    # or similar
    while(reference_exists(reference)):
        reference = __generate_reference(now)

    return reference

# Name scrambled to avoid direct calls
def __generate_reference(now):
    
    # Marked in upper case to denote constants
    ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ALPHANUMERIC = ALPHA + "0123456789"

    # Can be amended if a longer reference is required
    SUFFIXLENGTH = 4
    
    # Supposes launch date is January 2021
    LAUNCHDATE = datetime(2021, 1, 1)

    monthsSinceLaunch = (now.year - LAUNCHDATE.year) * 12 + (now.month - LAUNCHDATE.month)

    # using // to ensure return is a floored integer
    firstCharIndex = monthsSinceLaunch // 26
    secondCharIndex = monthsSinceLaunch % 26

    firstChar = ALPHA[firstCharIndex]
    secondChar = ALPHA[secondCharIndex]

    suffix = ''

    for _ in range(SUFFIXLENGTH):
        suffix = suffix + (random.choice(ALPHANUMERIC))

    reference = firstChar + secondChar + suffix

    return reference

def reference_exists(reference):
    
    try:
        reference = SyncRequest.objects.get(reference=reference)
        return True
    except SyncRequest.DoesNotExist:
        return False
    