from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from datetime import date
from passlib.hash import pbkdf2_sha256
from django.conf import settings
from .services import *
from .models import *
from .forms import *
# Create your views here.





