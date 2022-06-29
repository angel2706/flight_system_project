from datetime import datetime
import datetime as dt
from datetime import date, timedelta
from .models import Flight, Departure, Arrival, Airport, Plane, City, Stop, Leg, Timezone, AvailableSeats


def create_leg(dep_airport, arr_airport, current_date, travel_time):

    new_dep = Departure(airport_fk=dep_airport, datetime=current_date)
    new_dep.save()

    current_date += travel_time

    new_arr = Arrival(airport_fk=arr_airport, datetime=current_date)
    new_arr.save()

    new_leg = Leg(depart_fk=new_dep, arrival_fk=new_arr)  # , leg_duration=)
    new_leg.save()

    return new_dep, new_arr, new_leg


def create_stop(stop_datetime, leave_datetime, stop_dest, stop_mins):

    new_stop = Stop(
        airport_fk=stop_dest,
        stop_time=stop_datetime,
        leave_time=leave_datetime,
        stop_duration=stop_mins
    )
    new_stop.save()

    return new_stop


def create_flight_with_stop(dep_airport, stop_airport, arr_airport,
                            first_departure_date, second_departure_date,
                            first_leg_travel_mins, second_leg_travel_mins, stop_mins,
                            plane, price, flight_num):

    first_leg_travel_time = timedelta(minutes=first_leg_travel_mins)
    second_leg_travel_time = timedelta(minutes=second_leg_travel_mins)

    # nzne to nzro # first departure
    first_dep, first_arr, first_leg = create_leg(dep_airport, stop_airport, first_departure_date,
                                                 first_leg_travel_time)

    # nzro to yssy
    second_dep, second_arr, second_leg = create_leg(stop_airport, arr_airport, second_departure_date,
                                                    second_leg_travel_time)

    # stop @ nzro
    stop = create_stop(first_arr.datetime, second_dep.datetime, stop_airport, stop_mins)

    duration = first_leg_travel_mins + second_leg_travel_mins + stop_mins

    new_flight = Flight(
        depart_fk=first_dep,
        arrival_fk=second_arr,
        plane_fk=plane,
        price=price,
        flight_number=flight_num,
        num_stops=1,
        flight_duration=duration
    )
    new_flight.save()

    new_flight.legs.add(first_leg)
    new_flight.stops.add(stop)
    new_flight.legs.add(second_leg)

    create_available_seats(new_flight, plane)


def create_flight(dep_airport, arr_airport, current_date, plane, price, flight_num, travel_mins):

    travel_time = timedelta(minutes=travel_mins)

    new_dep, new_arr, new_leg = create_leg(dep_airport, arr_airport, current_date, travel_time)

    new_flight = Flight(
            depart_fk=new_dep,
            arrival_fk=new_arr,
            plane_fk=plane,
            price=price,
            flight_number=flight_num,
            num_stops=0,
            flight_duration=travel_mins
    )

    new_flight.save()
    new_flight.legs.add(new_leg)

    create_available_seats(new_flight, plane)


def create_available_seats(flight, plane):

    capacity = plane.capacity

    new_avail = AvailableSeats(flight_fk=flight, capacity=capacity)
    new_avail.save()

