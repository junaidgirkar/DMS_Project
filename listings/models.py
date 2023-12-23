from django.db import models
from django.contrib.auth.models import User

# Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=100)
    address = models.TextField()
    credit_score = models.IntegerField()
    income = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name()

# HouseOwner model
class HouseOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()

# Agent model
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=100)
    address = models.TextField()
    brokerage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name()

# Agency model
class Agency(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    email_id = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

# Guarantor model
class Guarantor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=100)
    address = models.TextField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField()

    def __str__(self):
        return self.user.get_full_name()

# Property model
class Property(models.Model):
    region_name = models.CharField(max_length=100)
    region_type = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    metro = models.CharField(max_length=100)
    county_name = models.CharField(max_length=100)
    year = models.IntegerField()
    owner = models.ForeignKey(HouseOwner, on_delete=models.CASCADE, related_name='properties')
    size = models.DecimalField(max_digits=6, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.region_name}, {self.city}"

# Listing model
class Listing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='listings')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings')
    is_for_rent = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{'Rent' if self.is_for_rent else 'Sale'} - {self.property.region_name}"

# Registration model
class Registration(models.Model):
    house_owner = models.ForeignKey(HouseOwner, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    guarantor = models.ForeignKey(Guarantor, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Registration for {self.listing.property.region_name}"

# Link Agent to Agency
Agent.add_to_class('agency', models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agents'))
