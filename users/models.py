from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime


# Create your models here.

def check_if_result_exist():
    """
    check if a customer have already submitted their reservation
    """
    pass


def number_customers_now():
    """
    check empty rooms
    """
    # customers = Customer.objects.all()
    # res = Customer.objects.filter(date_to__date__lte=date_to, date_from__date__gte=date_from).filter(
    #    surname="da")
    pass


def number_available_rooms(num_customers, accommodation):
    if accommodation == "cabin":
        return 1 - num_customers
    if accommodation == "bunkhouse room":
        return 7 - num_customers
    if accommodation == "deluxe bunkhouse room":
        return 2 - num_customers
    if accommodation == "powered site":
        return 30 - num_customers
    if accommodation == "unpowered site":
        return 100 - num_customers


def check_availability(date, accommodation):
    num_customers = Customer.objects.filter(date_from__date__lte=date, date_to__date__gte=date) \
        .filter(accommodation=accommodation)
    num_customers = len(num_customers)
    if accommodation == "cabin":
        if number_available_rooms(num_customers, accommodation) == 0:
            return False
        print(number_available_rooms(num_customers, accommodation))
        return True
    if accommodation == "bunkhouse room":
        if number_available_rooms(num_customers, accommodation) == 0:
            return False
        print(number_available_rooms(num_customers, accommodation))
        return True
    if accommodation == "deluxe bunkhouse room":
        if number_available_rooms(num_customers, accommodation) == 0:
            return False
        print(number_available_rooms(num_customers, accommodation))
        return True
    if accommodation == "powered site":
        if number_available_rooms(num_customers, accommodation) == 0:
            return False
        print(number_available_rooms(num_customers, accommodation))
        return True
    if accommodation == "unpowered site":
        if number_available_rooms(num_customers, accommodation) == 0:
            return False
        print(number_available_rooms(num_customers, accommodation))
        return True



def check_validity_of_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def create_record(name, surname, phone=None, email=None, date_from=None, date_to=None, accommodation=None,
                  no_rooms_sites=None, adults=None, kids=None):
    """
    create new record
    """
    Customer.objects.create(name=name, surname=surname, phone=phone, email=email, date_from=date_from,
                            date_to=date_to, accommodation=accommodation, no_rooms_sites=no_rooms_sites,
                            adults=adults, kids=kids)


class Customer(models.Model):
    """
    data oriented class
    """
    booking_created = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = PhoneNumberField(null=True, blank=False)
    email = models.EmailField(null=True, blank=True)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    accommodation = models.CharField(null=True, blank=True, max_length=50)
    no_rooms_sites = models.IntegerField(default=1)
    adults = models.IntegerField(default=0, null=True, blank=True)
    kids = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.booking_created}, {self.name}, {self.surname}, {self.phone}, {self.email}," \
               f" {self.date_from}, {self.date_to}, {self.accommodation}, {self.no_rooms_sites}," \
               f" {self.adults}, {self.kids}"
