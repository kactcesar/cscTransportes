
from django.urls import reverse
from .models import *
from django.shortcuts import render
from django.contrib.auth.models import auth


def index(request):
    return render(request, 'cscbase/base.html')
