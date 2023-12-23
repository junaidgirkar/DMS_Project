from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Customer, HouseOwner, Agent, Agency, Guarantor, Property, Listing, Registration

# Inline admin for Customer, HouseOwner, Agent, and Guarantor
class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customer'

class HouseOwnerInline(admin.StackedInline):
    model = HouseOwner
    can_delete = False
    verbose_name_plural = 'house owner'

class AgentInline(admin.StackedInline):
    model = Agent
    can_delete = False
    verbose_name_plural = 'agent'

class GuarantorInline(admin.StackedInline):
    model = Guarantor
    can_delete = False
    verbose_name_plural = 'guarantor'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline, HouseOwnerInline, AgentInline, GuarantorInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Agency)
admin.site.register(Registration)

# Optionally, you can customize the admin for specific models
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'city', 'state_name', 'owner')
    list_filter = ('city', 'state_name')
    search_fields = ('region_name', 'city')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'agent', 'is_for_rent', 'is_sold', 'is_active')
    list_filter = ('is_for_rent', 'is_sold', 'is_active')
    search_fields = ('property__region_name',)

# Apply custom admin classes
admin.site.register(Property, PropertyAdmin)
admin.site.register(Listing, ListingAdmin)
