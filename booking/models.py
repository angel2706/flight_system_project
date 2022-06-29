from django.db import models
from flights.models import Flight
from users.models import Customer


# Create your models here.
class Booking(models.Model):
    reference_number = models.CharField(max_length=200, unique=True)
    flight_fk = models.ForeignKey('flights.Flight', on_delete=models.CASCADE)
    booked_time = models.DateTimeField()

    # one to many - one customer to many bookings
    customer_id = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
