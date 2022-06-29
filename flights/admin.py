from django.contrib import admin
from .models import Flight, Departure, Arrival, Airport, Plane, City, Timezone, Stop, Leg, AvailableSeats

# Register your models here.
flight_models = [Flight, Departure, Arrival, Airport, Plane, City, Timezone, Stop, Leg, AvailableSeats]

admin.site.register(flight_models)
