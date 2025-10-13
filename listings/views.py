from django.shortcuts import render
from .models import Listing

def home(request):
    listings = Listing.objects.filter(status="published")[:50]
    return render(request, "home.html", {"listings": listings})