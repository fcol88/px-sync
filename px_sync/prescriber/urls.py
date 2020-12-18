"""
URL mapping list
"""

from django.urls import path

from . import views

urlpatterns = [

    path('login', views.login_page, name="login"),

    path('logout', views.logout_page, name="logout"),

    path('search', views.request_search, name="search"),

    path('view/<int:sync_id>', views.view_request, name="viewrequest")

]
