from django.urls import path

from . import views

urlpatterns = [
    path('start', views.landing, name="landing"),
    path('start/<str:found>', views.landing, name="notfound"),
    path('resume', views.resume, name="resume"),
    path('reference', views.reference, name="reference"),
    path('prescriptions', views.prescriptions, name="prescriptions"),
    path('viewprescription', views.viewprescription, name="viewprescription"),
    path('frequency', views.frequency, name="frequency"),
    path('calculate', views.calculate, name='calculate'),
]