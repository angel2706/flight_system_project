from flights.models import Flight, AvailableSeats
from users.models import Customer
from .models import Booking
from datetime import datetime
from random import randint

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def book_flight(request):

    if request.method == "POST":

        request.session['flight_id'] = request.POST['flight_id']

        return redirect("create-booking-invoice")

    flight_id = request.session["flight_id"]
    flight = Flight.objects.get(id=flight_id)
    flight_info = {'flight':flight}

    return render(request, 'booking/book_flight.html', flight_info)


@login_required()
def create_booking_invoice(request):

    flight_id = request.session["flight_id"]
    flight = Flight.objects.get(id=flight_id)

    # get users customer object
    username = request.user.username
    customer = Customer.objects.get(username=username)

    # create booking reference number
    ref_num = hash(str(flight.id) + str(customer.username) + str(randint(1, 1001)))
    if ref_num < 0:
        ref_num = ref_num * -1

    # booked time
    booked_time = datetime.now()

    # create and save booking
    # to prevent dups, dont re-create bookings
    booking = Booking(reference_number=ref_num, flight_fk=flight, customer_id=customer, booked_time=booked_time)
    booking.save()

    # update available seats for flight
    seats_left = AvailableSeats.objects.get(flight_fk=flight)
    seats_left.capacity -= 1
    seats_left.save()

    request.session["ref_num"] = ref_num

    return redirect('view-booking-invoice')


@login_required()
def view_bookings(request):

    if request.method == "POST":

        request.session["ref_num"] = request.POST["ref_num"]

        return redirect('view-booking-invoice')

    username = request.user.username
    customer = Customer.objects.get(username=username)

    all_bookings = Booking.objects.filter(customer_id=customer)

    page_information = {
        'booking_info': all_bookings
    }

    return render(request, 'booking/bookings.html', page_information)


@login_required()
def view_booking_invoice(request):

    if request.method == "POST":

        to_cancel = request.session["ref_num"]

        booked = Booking.objects.get(reference_number=to_cancel)

        flight = Flight.objects.get(id=booked.flight_fk.id)
        avail_seats = AvailableSeats.objects.get(flight_fk=flight)
        avail_seats.capacity += 1
        avail_seats.save()

        booked.delete()

        return redirect("cancelled-booking")

    ref_num = request.session["ref_num"]
    booking = Booking.objects.get(reference_number=ref_num)

    return render(request, 'booking/invoice.html', {'booking': booking})


@login_required()
def cancelled_booking(request):
    ref_num = request.session["ref_num"]

    return render(request, 'booking/cancelled.html', {'ref_num': ref_num})




