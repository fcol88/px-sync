"""
URL mapping list
"""

from django.urls import path

from . import views

urlpatterns = [
    path('start', views.landing, name="start"),

    path('start/<str:status>', views.landing, name="startwithstatus"),

    path('resume', views.resume, name="resume"),

    path('reference', views.create_sync_request, name="reference"),

    path('prescriptions', views.list_prescriptions, name="prescriptions"),

    path('prescription/<int:prescription_id>', views.view_prescription,
    name="prescription"),

    path('frequency', views.frequency_form, name="frequency"),

    path('frequency/<int:prescription_id>', views.frequency_form,
    name="editfrequency"),

    path('itemname/<int:prescription_id>', views.item_name_form,
    name="itemname"),

    path('itemname/<int:prescription_id>/<int:quantity_id>',
    views.item_name_form, name="edititemname"),

    path('dosage/<int:quantity_id>', views.dosage_form, name="dosage"),

    path('stock/<int:quantity_id>', views.stock_form, name="stock"),

    path('checkitems/<int:prescription_id>', views.check_items,
    name="checkitems"),

    path('calculate', views.calculate, name='calculate'),

    path('syncrequest', views.view_sync_request, name='syncrequest')
]
