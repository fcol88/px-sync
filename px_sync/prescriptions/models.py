"""
Database objects for prescription sync application
"""

from django.db import models

class SyncRequest(models.Model):
    """
    SyncRequest.reference = a generated 6 character string
    """
    reference = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now=True)

class Prescription(models.Model):
    """
    Prescription.frequency = frequency in days of prescription
    """
    syncRequest = models.ForeignKey('SyncRequest', on_delete=models.CASCADE)
    frequency = models.SmallIntegerField(default=0)

class Quantity(models.Model):
    """
    Quantity.dosage = the amount taken per period
    Quantity.period = the frequency the dosage is taken
    Quantity.perDay = computed from dosage and period
    Quantity.inStock = the amount the patient has
    Quantity.required = the computed amount required
    """
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    dosage = models.SmallIntegerField(default=-1)
    period = models.SmallIntegerField(default=-1)
    perDay = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    inStock = models.SmallIntegerField(default=-1)
    required = models.SmallIntegerField(default=0)
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE)

class Drug(models.Model):
    """
    A drug will be created irrespective of whether
    the exact text exists in the database presently.
    This is because small variations in user entry
    will obfuscate LOWER(name) LIKE and other similar
    non-fuzzy string matching.
    Longer term, this is a candidate for replacing with
    a link to the DM+D/CDR API, at which point this will
    store the unique AMPP ID, an integer which is easier
    to match on.
    """
    name = models.CharField(max_length=200)
