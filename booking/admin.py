from django.contrib import admin
from .models import Booking

# Register your models here.
booking_models = [Booking]

admin.site.register(booking_models)