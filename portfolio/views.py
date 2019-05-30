from django.shortcuts import render
from .models import portfolio

# Create your views here.
def portfolio(request):
    portfolio=Portfolio.objects
    return render(request, 'portfolio.html', {'portfolios':portfolio})