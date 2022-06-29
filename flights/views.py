from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime
from .create_data import *
from .models import Flight, Departure, Arrival, Airport, Plane, City, Stop, Leg, AvailableSeats
from .create_flight_functions import create_leg, create_stop, create_flight_with_stop, create_flight, \
    create_available_seats

from django.core.paginator import Paginator


# If you for some reason need to run the populate stuff, they take ages, just give it time
# especially the flight one, like a solid few minutes
def populate_base_data(request):
    create_base_data()

    return search(request)


def populate_data(request):

    # adjust dates to create more
    # uncomment flights if commented
    start_date = datetime(2022, 7, 30)
    end_date = datetime(2022, 8, 30)

    # ran 27-06-22 till 30-07-22 not inclusive of last date
    # ran 30-07-22 till 30-08-22 not inclusive of last date

    df_airport = Airport.objects.get(airport_code="NZNE")

    create_nzne_to_nzro(start_date, end_date, df_airport)
    create_nzne_to_nztl(start_date, end_date, df_airport)
    create_nzne_to_nzgb(start_date, end_date, df_airport)
    create_nzne_to_nzci(start_date, end_date, df_airport)
    create_nzne_to_nzro_to_yssy(start_date, end_date, df_airport)

    return search(request)


# Create your views here
def search(request):

    places = City.objects.all()

    if request.method == "POST":
        request.session['depart_place'] = request.POST['depart_place']
        request.session['arrive_place'] = request.POST['arrive_place']
        request.session['depart_time'] = request.POST['depart_time']

        return redirect('results')

    return render(request, 'flights/search.html', {'places': places})


def results(request):

    if request.method == "POST":
        request.session['flight_id'] = request.POST['flight_id']

        return redirect('book-flight')

    # VALIDATE PLACE INPUT
    places = City.objects.all()

    depart_place = request.session['depart_place']
    arrive_place = request.session['arrive_place']

    validated_from = False
    validated_to = False

    for allowed_place in places:

        new_place = str(allowed_place.city_name) + ", " + str(allowed_place.country)

        if depart_place == new_place:
            validated_from = True
        if arrive_place == new_place:
            validated_to = True

    if validated_to and validated_from:

        d_place_break = depart_place.split(", ")
        d_city_val = d_place_break[0]
        d_country_val = d_place_break[1]

        d_city = City.objects.get(city_name=d_city_val, country=d_country_val)

        # GET ARRIVAL CITY
        a_place_break = arrive_place.split(", ")
        a_city_val = a_place_break[0]
        a_country_val = a_place_break[1]

        a_city = City.objects.get(city_name=a_city_val, country=a_country_val)

        dep_time = request.session['depart_time']

        dep_datetime = create_datetime(dep_time, "0:0")

        # GET MATCHES
        available_flights = AvailableSeats.objects.filter(
            flight_fk__depart_fk__airport_fk__city_fk=d_city,
            flight_fk__arrival_fk__airport_fk__city_fk=a_city,
            flight_fk__depart_fk__datetime__gt=dep_datetime
        )

        paginator = Paginator(available_flights, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'available_flights': available_flights,
            'page_obj':page_obj,
            'places': places
        }

        return render(request, 'flights/results.html', context)

    else:
        error = {'error':"Invalid place! Please select from the suggested options"}
        return render(request, 'flights/search.html', error)


def create_datetime(date, time):
    broken_date = date.split('-')
    broken_time = time.split(':')

    # datetime(year, month, day, hour, minute, second, microsecond)
    new_datetime = datetime(
        int(broken_date[0]), int(broken_date[1]), int(broken_date[2]),  # date
        int(broken_time[0]), int(broken_time[1]), 0, 0  # time
    )

    return new_datetime


# ignore everything below

# def create_new_flight(request):
#     return render(request, 'flights/create_flight.html')
#

# def create_multi(request):
#
#     if request.method == "POST":
#         # -- SAVE Request data to variables
#         flight_price = request.POST['flight_price']
#         flight_num = request.POST['flight_num']
#         plane = request.POST['plane']
#
#         first_depart_place = request.POST['first_depart_place']
#         first_depart_date = request.POST['first_depart_date']
#         first_depart_time = request.POST['first_depart_time']
#
#         second_arrive_place = request.POST['second_arrive_place']
#         second_arrive_date = request.POST['second_arrive_date']
#         second_arrive_time = request.POST['second_arrive_time']
#
#         num_stops = 1
#         stop_dest = request.POST['stop_dest']
#         stop_date = request.POST['stop_date']
#         stop_time = request.POST['stop_time']
#         leave_date = request.POST['leave_date']
#         leave_time = request.POST['leave_time']
#
#         # -- SAVE Request data to session for later use
#         request.session['flight_price'] = flight_price
#         request.session['flight_num'] = flight_num
#         request.session['plane'] = plane
#
#         request.session['first_depart_place'] = first_depart_place
#         request.session['first_depart_date'] = first_depart_date
#         request.session['first_depart_time'] = first_depart_time
#
#         request.session['second_arrive_place'] = second_arrive_place
#         request.session['second_arrive_date'] = second_arrive_date
#         request.session['second_arrive_time'] = second_arrive_time
#
#         request.session['num_stops'] = num_stops
#         request.session['stop_dest'] = stop_dest
#         request.session['stop_date'] = stop_date
#         request.session['stop_time'] = stop_time
#         request.session['leave_date'] = leave_date
#         request.session['leave_time'] = leave_time
#
#         # -- FIRST DEPARTURE CREATION
#         first_d_datetime = create_datetime(first_depart_date, first_depart_time)
#         first_new_dep = create_new_departure(first_d_datetime, first_depart_place)
#         first_new_dep.save()
#
#         # -- FIRST ARRIVAL CREATION
#         first_a_datetime = create_datetime(stop_date, stop_time)
#         first_new_arr = create_new_arrival(first_a_datetime, stop_dest)
#         first_new_arr.save()
#
#         # -- SECOND DEPARTURE CREATION
#         second_d_datetime = create_datetime(leave_date, leave_time)
#         second_new_dep = create_new_departure(second_d_datetime, stop_dest)
#         second_new_dep.save()
#
#         # -- SECOND ARRIVAL CREATION
#         second_a_datetime = create_datetime(second_arrive_date, second_arrive_time)
#         second_new_arr = create_new_arrival(second_a_datetime, second_arrive_place)
#         second_new_arr.save()
#
#         # -- LEG CREATIONS
#         first_leg = Leg(depart_fk=first_new_dep, arrival_fk=first_new_arr)
#         first_leg.save()
#
#         second_leg = Leg(depart_fk=second_new_dep, arrival_fk=second_new_arr)
#         second_leg.save()
#
#         # -- PLANE RETREIVAL
#         flight_plane = Plane.objects.get(plane_id=plane)
#
#         # STOP CREATION
#         stop_datetime = create_datetime(stop_date, stop_time)
#         leave_datetime = create_datetime(leave_date, leave_time)
#         new_stop_airport = Airport.objects.get(airport_code=stop_dest)
#         new_stop = Stop(
#             airport_fk=new_stop_airport,
#             stop_time=stop_datetime,
#             leave_time=leave_datetime # , stop_duration=
#         )
#         new_stop.save()
#
#         new_flight = Flight(
#             depart_fk=first_new_dep,
#             arrival_fk=second_new_arr,
#             plane_fk=flight_plane,
#             price=flight_price,
#             flight_number=flight_num,
#             num_stops=num_stops # , flight_duration=flight_duration)
#         )
#         new_flight.save()
#
#         new_flight.legs.add(first_leg)
#         new_flight.legs.add(second_leg)
#         new_flight.stops.add(new_stop)
#
#         return redirect('created-multi')
#
#     return render(request, 'flights/create_multi.html')
#
#
# def create_nonstop(request):
#
#     if request.method == "POST":
#         # -- SAVE Request data to variables
#         depart_place = request.POST['depart_place']
#         arrive_place = request.POST['arrive_place']
#
#         depart_date = request.POST['depart_date']
#         arrive_date = request.POST['arrive_date']
#
#         depart_time = request.POST['depart_time']
#         arrive_time = request.POST['arrive_time']
#
#         flight_price = request.POST['flight_price']
#         flight_num = request.POST['flight_num']
#         plane = request.POST['plane']
#
#         # -- SAVE Request data to session for later use
#         request.session['depart_place'] = depart_place
#         request.session['arrive_place'] = arrive_place
#
#         request.session['depart_time'] = depart_time
#         request.session['arrive_time'] = arrive_time
#
#         request.session['depart_date'] = depart_date
#         request.session['arrive_date'] = arrive_date
#
#         request.session['flight_price'] = flight_price
#         request.session['flight_num'] = flight_num
#         request.session['plane'] = plane
#
#         # -- DEPARTURE CREATION
#         d_datetime = create_datetime(depart_date, depart_time)
#         new_dep = create_new_departure(d_datetime, depart_place)
#         new_dep.save()
#
#         # -- ARRIVAL CREATION
#         a_datetime = create_datetime(arrive_date, arrive_time)
#         new_arr = create_new_arrival(a_datetime, arrive_place)
#         new_arr.save()
#
#         # -- LEG CREATION
#         # !!-- calculate duration
#         new_leg = Leg(depart_fk=new_dep, arrival_fk=new_arr)  # , leg_duration=)
#         new_leg.save()
#
#         # -- PLANE RETREIVAL
#         flight_plane = Plane.objects.get(plane_id=plane)
#
#         # -- FLIGHT CREATION
#         new_flight = Flight(
#             depart_fk=new_dep,
#             arrival_fk=new_arr,
#             plane_fk=flight_plane,
#             price=flight_price,
#             flight_number=flight_num,
#             num_stops=0  # ,flight_duration=flight_duration)
#         )
#         new_flight.save()
#
#         new_flight.legs.add(new_leg)
#
#         return redirect('created-nonstop')
#
#     return render(request, 'flights/create_nonstop.html')


# def create_new_departure(d_dt, d_place):
#     d_airport = Airport.objects.get(airport_code=d_place)
#     new_dep = Departure(airport_fk=d_airport, datetime=d_dt)
#
#     return new_dep
#
#
# def create_new_arrival(a_dt, a_place):
#     a_airport = Airport.objects.get(airport_code=a_place)
#     new_arr = Arrival(airport_fk=a_airport, datetime=a_dt)
#
#     return new_arr


# def create_nonstop_results(request):
#
#     new_nonstop = {
#         'depart_place': request.session['depart_place'],
#         'arrive_place': request.session['arrive_place'],
#
#         'depart_time': request.session['depart_time'],
#         'arrive_time': request.session['arrive_time'],
#
#         'depart_date': request.session['depart_date'],
#         'arrive_date': request.session['arrive_date'],
#
#         'flight_price': request.session['flight_price'],
#         'flight_num': request.session['flight_num'],
#         'plane': request.session['plane']
#     }
#
#     return render(request, 'flights/create_nonstop_results.html', new_nonstop)
#
#
# def create_multi_results(request):
#
#     new_nonstop = {
#         'flight_price': request.session['flight_price'],
#         'flight_num': request.session['flight_num'],
#         'plane': request.session['plane'],
#
#         'first_depart_place': request.session['first_depart_place'],
#         'first_depart_date': request.session['first_depart_date'],
#         'first_depart_time': request.session['first_depart_time'],
#
#         'second_arrive_place': request.session['second_arrive_place'],
#         'second_arrive_date': request.session['second_arrive_date'],
#         'second_arrive_time': request.session['second_arrive_time'],
#
#         'num_stops': request.session['num_stops'],
#         'stop_dest': request.session['stop_dest'],
#         'stop_date': request.session['stop_date'],
#         'stop_time': request.session['stop_time'],
#         'leave_date': request.session['leave_date'],
#         'leave_time': request.session['leave_time'],
#     }
#
#     return render(request, 'flights/create_multi_results.html', new_nonstop)






 # STOP DURATION
        # stop_diff = leave_datetime - stop_datetime
        # s_seconds = stop_diff.total_seconds()
        # s_hours = s_seconds // 3600
        # s_minutes = (s_seconds % 3600) // 60
        #
        # stop_duration = "{} hr {} min".format(s_hours, s_minutes)
        # request.session['stop_duration'] = stop_duration
        #
        # # FLIGHT DURATION - with consideration for stop
        # first_half_diff = stop_datetime - d_datetime
        # first_half_seconds = first_half_diff.total_seconds()
        # first_half_hours = first_half_seconds // 3600
        # first_half_minutes = (first_half_seconds % 3600) // 60
        #
        # second_half_diff = a_datetime - leave_datetime
        # second_half_seconds = second_half_diff.total_seconds()
        # second_half_hours = second_half_seconds // 3600
        # second_half_minutes = (second_half_seconds % 3600) // 60
        #
        # combined_hours = s_hours + first_half_hours + second_half_hours
        # totalled_mins = s_minutes + first_half_minutes + second_half_minutes
        #
        # # re format the collected minutes
        # flight_duration_minutes = totalled_mins % 60
        # combined_hours += totalled_mins // 60
        #
        # flight_duration = "{} hr {} min".format(combined_hours, flight_duration_minutes)
        # request.session['flight_duration'] = flight_duration


# request.session['first_arrive_place'] = first_arrive_place
# request.session['first_arrive_date'] = first_arrive_date
# request.session['first_arrive_time'] = first_arrive_time

# request.session['second_depart_place'] = second_depart_place
# request.session['second_depart_date'] = second_depart_date
# request.session['second_depart_time'] = second_depart_time


# first_arrive_place = request.POST['first_arrive_place']
# first_arrive_date = request.POST['first_arrive_date']
# first_arrive_time = request.POST['first_arrive_time']

# second_depart_place = request.POST['second_depart_place']
# second_depart_date = request.POST['second_depart_date']
# second_depart_time = request.POST['second_depart_time']