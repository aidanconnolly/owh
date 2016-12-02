from django.shortcuts import render
from myproject.bills.models import *
from django.http import HttpResponse

# Create your views here.

def index(request):
    bills = Bill.objects.all()
    return render(request, 'bills/index.html', {'bills':bills})