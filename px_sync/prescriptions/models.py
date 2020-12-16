from django.db import models

# SyncRequest.reference = a generated 6 character string
class SyncRequest(models.Model):
    reference = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now=True)

# Prescription.frequency = frequency in days of prescription
class Prescription(models.Model):
    syncRequest = models.ForeignKey('SyncRequest', on_delete=models.CASCADE)
    frequency = models.SmallIntegerField(default=0)

# Quantity.prescribed - the amount present on a prescription
# Quantity.inStock = the amount the patient has
# Quantity.required = the computed amount required
class Quantity(models.Model):
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    dosage = models.SmallIntegerField(default=-1)
    period = models.SmallIntegerField(default=-1)
    perDay = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    inStock = models.SmallIntegerField(default=-1)
    required = models.SmallIntegerField(default=0)
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE)

# A drug will be created irrespective of whether
# the exact text exists in the database presently.
# This is because small variations in user entry
# will obfuscate LOWER(name) LIKE and other similar
# non-fuzzy string matching.
# Longer term, this is a candidate for replacing with
# a link to the DM+D/CDR API, at which point this will
# store the unique AMPP ID, an integer which is easier
# to match on.
class Drug(models.Model):
    name = models.CharField(max_length=200)
