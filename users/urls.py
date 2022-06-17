
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('customer', views.customer, name="customer"),
    path('send_emails', views.send_emails, name="send_emails")

]
