from celery import shared_task

# default smtp email submission port
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import smtplib
import csv
from datetime import datetime


from .models import Customer
# lets demonstrate how celery is asynchronous
# decorator

@shared_task
def send_email_to_customer(name,email):
    # todo first two lines just for celery

    port = 587
    smtp_server = "smtp-mail.outlook.com"
    sender_email = "hamrozipetr@outlook.com"  # Enter your address
    receiver_email = str(email)  # Enter receiver address
    password = "Pumpkin1998"
    message = MIMEMultipart()
    message["Subject"] = "Booking Lorne Station"
    text = f"""
    Dear {name.capitalize()},
    Your booking at Lorne Holiday Station was successful.
    Enjoy your stay.

    Yours faithfully, 

    Damien Waterford
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    try:
        # Create a secure SSL context
        # context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"the problem is: {e}")


@shared_task
def generate_csv():
    """
    generate spreadsheet for the owner always update it
    https://shahidzoonimar.medium.com/how-to-create-a-csv-and-send-in-the-email-attachment-with-django-cb6b252094d7
    """
    customers = Customer.objects.all()
    filename = "booking.csv"
    with open(filename, "w") as csvfile:
        cr = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        cr.writerow(['booking date', 'name', 'surname', 'phone', 'email', 'date from', 'date to', 'accommodation',
                     'number of rooms/places', 'adults', 'kids'])
        for customer in customers:
            date_from = datetime.strftime(customer.date_from, "%d/%m/%Y")
            date_to = datetime.strftime(customer.date_to, "%d/%m/%Y")
            booking = datetime.strftime(customer.booking_created, "%d/%m/%Y")

            cr.writerow([booking, customer.name, customer.surname,customer.phone,customer.email, date_from, date_to,
                         customer.accommodation, customer.no_rooms_sites, customer.adults, customer.kids])
    csvfile.close()
    send_email_to_owner(filename)



@shared_task
def send_email_to_owner(filename):
    """
    send an update of all booking
    """

    port = 587
    smtp_server = "smtp-mail.outlook.com"
    sender_email = "hamrozipetr@outlook.com"  # Enter your address
    receiver_email = "hamrozipetr@outlook.com"  # Enter receiver address
    password = "Pumpkin1998"
    message = MIMEMultipart()
    message["Subject"] = "Booking Lorne Station for Damien"
    text = f"""
        Dear Damien,
        just update of all booking

        Yours faithfully, 

        Petr Hamrozi
        """
    email = "hamrozipetr@outlook.com"

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add body to email
    message.attach(MIMEText(text, "plain"))

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    try:
        # Create a secure SSL context
        # context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"the problem is: {e}")
