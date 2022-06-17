from django.shortcuts import render, HttpResponse, redirect

from django.conf import settings
import asyncio
from asgiref.sync import sync_to_async
# Create your views here.

from .tasks import sleepy, send_email_task

def index(request):
    send_email_task.delay()
    return HttpResponse('<h1> Email is sent much faster! </h1>')


