import os
import django
import random
from faker import Faker

# Configure settings for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydialogflowproject.settings')
django.setup()

from django.contrib.auth.models import User
from listings.models import HouseOwner, Property, Agent, Agency, Listing, Customer, Guarantor, Registration

fake = Faker()

def create_user():
    username = fake.user_name()
    while User.objects.filter(username=username).exists():
        username = fake.user_name()
    email = fake.email()
    password = 'testpassword123'  # Use a safer password in production
    return User.objects.create_user(username=username, email=email, password=password)

def create_agencies(n):
    agencies = [Agency(name=fake.company(), phone_no=fake.phone_number(), email_id=fake.email(), address=fake.address()) for _ in range(n)]
    Agency.objects.bulk_create(agencies)
    return Agency.objects.all()

def create_agents(agencies, n):
    for _ in range(n):
        user = create_user()
        Agent.objects.create(user=user, phone_no=fake.phone_number(), address=fake.address(), brokerage=round(random.uniform(1.5, 3.5), 2), agency=random.choice(agencies))

def create_house_owners(n):
    for _ in range(n):
        user = create_user()
        HouseOwner.objects.create(user=user, phone_no=fake.phone_number(), address=fake.address())

def create_properties(n, house_owners):
    for _ in range(n):
        Property.objects.create(
            region_name=fake.city(), region_type='Urban', state_name=fake.state(), city=fake.city(), metro=fake.city() + ' Metro', 
            county_name=fake.city(), year=random.randint(1990, 2021), owner=random.choice(house_owners), 
            size=round(random.uniform(1200, 4500), 2), bedrooms=random.randint(2, 6), 
            bathrooms=round(random.uniform(1, 4), 1), price=round(random.uniform(100000, 500000), 2))

def create_listings(properties, agents):
    for property in properties:
        Listing.objects.create(
            property=property, agent=random.choice(agents) if agents else None, 
            is_for_rent=random.choice([True, False]), is_sold=not random.choice([True, False]), 
            is_active=random.choice([True, False]))

def create_customers(n):
    for _ in range(n):
        user = create_user()
        Customer.objects.create(
            user=user, phone_no=fake.phone_number(), address=fake.address(), 
            credit_score=random.randint(300, 850), income=round(random.uniform(30000, 200000), 2))

def create_guarantors(n):
    for _ in range(n):
        user = create_user()
        Guarantor.objects.create(
            user=user, phone_no=fake.phone_number(), address=fake.address(), 
            income=round(random.uniform(30000, 200000), 2), credit_score=random.randint(300, 850))

def create_registrations(customers, guarantors, listings):
    for _ in range(len(listings)):
        Registration.objects.create(
            house_owner=random.choice(HouseOwner.objects.all()), customer=random.choice(customers), 
            guarantor=random.choice(guarantors), agent=random.choice(Agent.objects.all()), 
            listing=random.choice(listings))

def populate_db():
    agencies = create_agencies(10)
    create_agents(agencies, 15)
    create_house_owners(20)
    create_customers(30)
    create_guarantors(20)
    create_properties(50, HouseOwner.objects.all())
    create_listings(Property.objects.all(), Agent.objects.all())
    create_registrations(Customer.objects.all(), Guarantor.objects.all(), Listing.objects.all())
    print("Database populated with sample data.")

if __name__ == '__main__':
    populate_db()
