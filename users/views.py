from django.shortcuts import render, HttpResponse, redirect

from django.conf import settings
import asyncio
from asgiref.sync import sync_to_async
# Create your views here.

from .tasks import send_all_emails
from django.shortcuts import render
from .models import create_record, check_validity_of_email, check_availability

from .models import Customer


def index(request):
    """
    home page
    """
    print("working")
    if request.method == "POST":
        name = request.POST['name']
        print(name)
    return render(request, "index.html")


def customer(request):
    """
    save data into database
    if everything is okay
    """
    print("function is working")
    invalid_email = False
    booked_out = False
    booking_accepted = False
    if request.method == "POST":
        try:
            # all variables
            name = request.POST['name']
            surname = request.POST['surname']
            phone = request.POST['phone']
            email = request.POST['email']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            accommodation = request.POST['accommodation']
            no_rooms_sites = request.POST['no_rooms_sites']
            adults = request.POST['adults']
            kids = request.POST['kids']

            print(name, surname, phone, email, date_from, date_to, adults, kids, accommodation,
                  no_rooms_sites)

            # check validity
            if check_validity_of_email(email):

                if check_availability(date_from, accommodation):

                    create_record(name, surname, phone, email, date_from, date_to, accommodation,
                                  no_rooms_sites, adults, kids)

                    print("this one is working")
                    booking_accepted = True
                    return render(request, "index.html", {'booking_accepted': booking_accepted})
                else:
                    booked_out = True
                    return render(request, "index.html", {'booked_out': booked_out})

            else:
                invalid_email = True
                return render(request, "index.html", {'invalid_email': invalid_email})

        except Exception as e:
            print(f"the problem is {e}")

    return render(request, "index.html")


def send_emails(request):
    """
    sending email to the owner with
    csv file of all booking and to a customer
    """

    last_customer = Customer.objects.all().last()
    name = last_customer.name
    email = last_customer.email
    #generate_csv.delay()
    #email = last_customer.email
    if request.method == "POST":
        # todo apply async code to get rid of the delay
        # confirmation email for customer
        # using celery to to create task queue
        send_all_emails.apply_async(args=[name, email])

        success = True
        # email for the owner including excel file
        return render(request, "index.html", {"success":success})
    else:
        return render(request, "index.html")
