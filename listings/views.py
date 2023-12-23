# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Property, Listing, HouseOwner
from django.views.decorators.csrf import csrf_exempt

# Home/Index View
def index(request):
    properties = Property.objects.all()
    return render(request, 'listings/index.html', {'properties': properties})

# Property Detail View
def property_detail(request, id):
    property = get_object_or_404(Property, pk=id)
    return render(request, 'listings/property_detail.html', {'property': property})

# User Registration View
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a desired page after successful registration
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# House Owner Profile View
@login_required
def house_owner_profile(request):
    try:
        house_owner = HouseOwner.objects.get(user=request.user)
    except HouseOwner.DoesNotExist:
        return redirect('index')  # Redirect to homepage or another page

    properties = Property.objects.filter(owner=house_owner)
    listings = Listing.objects.filter(property__in=properties)

    context = {
        'house_owner': house_owner,
        'properties': properties,
        'listings': listings
    }

    return render(request, 'listings/house_owner_profile.html', context)

# Add more views as needed for your application
