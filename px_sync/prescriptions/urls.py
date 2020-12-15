from django.urls import path

from . import views

urlpatterns = [
    path('start', views.landing, name="start"),
    path('start/<str:status>', views.landing, name="startwithstatus"),
    path('resume', views.resume, name="resume"),
    path('reference', views.reference, name="reference"),
    path('prescriptions', views.list_prescriptions, name="prescriptions"),
    path('prescription/<int:id>', views.view_prescription, name="prescription"),
    path('frequency', views.prescription_frequency, name="frequency"),
    path('frequency/<int:id>', views.prescription_frequency, name="editfrequency"),
    path('itemname/<int:prescriptionId>', views.item_name, name="itemname"),
    path('itemname/<int:prescriptionId>/<int:id>', views.item_name, name="edititemname"),
    path('dosage/<int:prescriptionId>/<int:drugId>', views.dosage, name="dosage"),
    path('dosage/<int:prescriptionId>/<int:drugId>/<int:id>', views.dosage, name="editdosage"),
    path('stock/<int:id>', views.stock, name="stock"),
    path('checkitems/<int:id>', views.check_items, name="checkitems"),
    path('calculate', views.calculate, name='calculate'),
]