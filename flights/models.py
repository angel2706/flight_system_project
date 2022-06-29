from django.db import models

# odd setup but good for the requirements!
# Rip to the hypothetical future developers having to restructure my db if the business does take off ;)))


class Flight(models.Model):
    depart_fk = models.ForeignKey('Departure', on_delete=models.CASCADE)
    arrival_fk = models.ForeignKey('Arrival', on_delete=models.CASCADE)

    plane_fk = models.ForeignKey('Plane', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    flight_number = models.CharField(max_length=6)  # flight numbers are made up by me
    flight_duration = models.DecimalField(max_digits=20, decimal_places=2)

    stops = models.ManyToManyField('Stop')
    num_stops = models.IntegerField()

    legs = models.ManyToManyField('Leg')

    def __str__(self):
        return str(self.id) + "  " + str(self.flight_number)


class Departure(models.Model):
    airport_fk = models.ForeignKey('Airport', on_delete=models.CASCADE)
    datetime = models.DateTimeField()


class Arrival(models.Model):
    airport_fk = models.ForeignKey('Airport', on_delete=models.CASCADE)
    datetime = models.DateTimeField()


class Leg(models.Model):
    depart_fk = models.ForeignKey('Departure', on_delete=models.CASCADE)
    arrival_fk = models.ForeignKey('Arrival', on_delete=models.CASCADE)

    def __str__(self):
        path = self.depart_fk.airport_fk.airport_code + " -> " + self.arrival_fk.airport_fk.airport_code
        return path


class Stop(models.Model):
    airport_fk = models.ForeignKey('Airport', on_delete=models.CASCADE)
    stop_time = models.DateTimeField()
    leave_time = models.DateTimeField()
    stop_duration = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.airport_fk.airport_code


class AvailableSeats(models.Model):
    flight_fk = models.ForeignKey('Flight', on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.flight_fk.id) + " " + str(self.flight_fk.flight_number) + " :" + \
               str(self.flight_fk.plane_fk.capacity)


class Airport(models.Model):
    # using ICAO
    airport_code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    city_fk = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.airport_code


class Plane(models.Model):
    plane_id = models.CharField(primary_key=True, max_length=25)
    capacity = models.IntegerField()
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.plane_id


# city is probs a bad name for this, should be more like area?? since I
# want it to include townships, small islands and stuff
# going with city anyway since it doesnt really matter, it more or less gets the point across
class City(models.Model):
    city_name = models.CharField(max_length=85)
    country = models.CharField(max_length=60)
    timezone_fk = models.ForeignKey('Timezone', on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class Timezone(models.Model):
    timezone_code = models.CharField(primary_key=True, max_length=6)
    timezone_name = models.CharField(max_length=40)
    gmt = models.CharField(max_length=9)

    def __str__(self):
        return self.timezone_code


