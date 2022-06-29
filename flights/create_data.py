from datetime import datetime
import datetime as dt
from datetime import date, timedelta
from .models import Flight, Departure, Arrival, Airport, Plane, City, Stop, Leg, Timezone, AvailableSeats
from .create_flight_functions import create_leg, create_stop, create_flight_with_stop, create_flight, \
    create_available_seats


# will create all the things like airports planes timezones etc
def create_base_data():
    populate_timezones()
    populate_planes()


def populate_timezones():

    nzst = Timezone(timezone_code="NZST", timezone_name="New Zealand Standard Time", gmt="GMT+12")
    nzst.save()

    aest = Timezone(timezone_code="AEST", timezone_name="Australian Eastern Standard Time", gmt="GMT+10")
    aest.save()

    chast = Timezone(timezone_code="CHAST", timezone_name="Chatham Island Standard Time", gmt="GMT+12:45")
    chast.save()

    populate_cities(nzst, aest, chast)


def populate_cities(nzst, aest, chast):

    rotorua = City(city_name="Rotorua", country="New Zealand", timezone_fk=nzst)
    auckland = City(city_name="Auckland", country="New Zealand", timezone_fk=nzst)
    great_barrier_island = City(city_name="Great Barrier Island", country="New Zealand", timezone_fk=nzst)
    chatham_island = City(city_name="Chatham Island", country="New Zealand", timezone_fk=chast)
    lake_tekapo = City(city_name="Lake Tekapo", country="New Zealand", timezone_fk=nzst)
    sydney = City(city_name="Sydney", country="Australia", timezone_fk=aest)

    rotorua.save()
    auckland.save()
    great_barrier_island.save()
    chatham_island.save()
    lake_tekapo.save()
    sydney.save()

    populate_airports(rotorua, auckland, great_barrier_island, chatham_island, lake_tekapo, sydney)


def populate_airports(rotorua, auckland, great_barrier_island, chatham_island, lake_tekapo, sydney):

    nzne = Airport(airport_code="NZNE", name="Dairy Flat Airport", city_fk=auckland)
    nzro = Airport(airport_code="NZRO", name="Rotorua Regional Airport", city_fk=rotorua)
    nztl = Airport(airport_code="NZTL", name="Lake Tekapo Airport", city_fk=lake_tekapo)
    nzcl = Airport(airport_code="NZCI", name="Tuuta Airport", city_fk=chatham_island)
    nzgb = Airport(airport_code="NZGB", name="Claris Airport", city_fk=great_barrier_island)
    yssy = Airport(airport_code="YSSY ", name="Sydney Airport", city_fk=sydney)

    nzne.save()
    nzro.save()
    nztl.save()
    nzcl.save()
    nzgb.save()
    yssy.save()


def populate_planes():

    syb001 = Plane(plane_id="Syb001", capacity=6, model="SyberJet SJ30i")
    cir001 = Plane(plane_id="Cir001", capacity=4, model="Cirrus SF50")
    cir002 = Plane(plane_id="Cir002", capacity=4, model="Cirrus SF50")
    hon001 = Plane(plane_id="Hon001", capacity=5, model="HondaJet Elite")
    hon002 = Plane(plane_id="Hon002", capacity=5, model="HondaJet Elite")

    syb001.save()
    cir001.save()
    cir002.save()
    hon001.save()
    hon002.save()


# below all used in populate-flights
def create_nzne_to_nzro(start_date, end_date, df_airport):
    # twice a day - monday to friday
    nzne_dep_times = [dt.time(6, 0, 0), dt.time(16, 0, 0)]
    nzro_dep_times = [dt.time(12, 0, 0), dt.time(18, 0, )]

    plane = Plane.objects.get(plane_id="Cir001")
    ro_place = "NZRO"

    ro_airport = Airport.objects.get(airport_code=ro_place)

    price = 90
    flight_num = "DF33"
    duration = 40

    current_date = start_date
    day_delta = timedelta(days=1)

    while current_date < end_date:

        for ne_dep_time in nzne_dep_times:

            new_date = datetime.combine(current_date, ne_dep_time)

            if new_date.isoweekday() != 6 and new_date.isoweekday() != 7:
                # return
                create_flight(dep_airport=df_airport, arr_airport=ro_airport,
                              current_date=new_date, plane=plane, price=price,
                              flight_num=flight_num,
                              travel_mins=duration)

        for ro_dep_time in nzro_dep_times:

            new_date = datetime.combine(current_date, ro_dep_time)

            if new_date.isoweekday() != 6 and new_date.isoweekday() != 7:

                # return
                create_flight(dep_airport=ro_airport, arr_airport=df_airport,
                              current_date=new_date, plane=plane, price=price,
                              flight_num=flight_num,
                              travel_mins=duration)

        current_date += day_delta


def create_nzne_to_nztl(start_date, end_date, df_airport):
    # once a week - depart monday and return friday
    nzne_dep_time = dt.time(8, 0, 0)
    nztl_dep_time = dt.time(13, 0, 0)

    plane = Plane.objects.get(plane_id="Hon001")

    lt_place = "NZTL"
    lt_airport = Airport.objects.get(airport_code=lt_place)

    price = 180
    flight_num = "DF52"
    duration = 95

    current_date = start_date
    day_delta = timedelta(days=1)
    travel_time = timedelta(minutes=duration)

    while current_date < end_date:

        if current_date.isoweekday() == 1:
            # if monday, depart df and arrive lake tekapo

            new_date = datetime.combine(current_date, nzne_dep_time)

            create_flight(dep_airport=df_airport, arr_airport=lt_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        if current_date.isoweekday() == 5:
            # if friday depart lake tekapo and arrive df

            new_date = datetime.combine(current_date, nztl_dep_time)

            create_flight(dep_airport=lt_airport, arr_airport=df_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        current_date += day_delta


def create_nzne_to_nzgb(start_date, end_date, df_airport):
    # three times a week,
    # depart nzne Monday, Wednesday, and Friday
    # depart nzgb Tuesday, Friday, and Saturday

    nzne_dep_time = dt.time(9, 0, 0)
    nzgb_dep_time = dt.time(8, 0, 0)

    plane = Plane.objects.get(plane_id="Cir002")

    gb_place = "NZGB"
    gb_airport = Airport.objects.get(airport_code=gb_place)

    price = 90
    flight_num = "DF96"
    duration = 10

    current_date = start_date
    day_delta = timedelta(days=1)
    travel_time = timedelta(minutes=duration)

    while current_date < end_date:

        # monday wednesday
        if current_date.isoweekday() == 1 or current_date.isoweekday() == 3:

            new_date = datetime.combine(current_date, nzne_dep_time)

            create_flight(dep_airport=df_airport, arr_airport=gb_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        # tuesday saturday
        if current_date.isoweekday() == 2 or current_date.isoweekday() == 6:

            new_date = datetime.combine(current_date, nzgb_dep_time)

            create_flight(dep_airport=gb_airport, arr_airport=df_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        # friday
        if current_date.isoweekday() == 5:

            new_date = datetime.combine(current_date, nzgb_dep_time)

            create_flight(dep_airport=gb_airport, arr_airport=df_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

            new_date = datetime.combine(current_date, nzne_dep_time)

            create_flight(dep_airport=df_airport, arr_airport=gb_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        current_date += day_delta


def create_nzne_to_nzci(start_date, end_date, df_airport):
    # twice weekly
    # depart nzne Tuesday and Friday
    # depart nzci Wednesday and Saturday

    nzne_dep_time = dt.time(11, 0, 0)
    nzci_dep_time = dt.time(12, 0, 0)

    plane = Plane.objects.get(plane_id="Hon002")

    ci_place = "NZCI"
    ci_airport = Airport.objects.get(airport_code=ci_place)

    price = 200
    flight_num = "DF26"
    duration = 150

    current_date = start_date
    day_delta = timedelta(days=1)
    travel_time = timedelta(minutes=duration)

    while current_date < end_date:

        # tuesday friday
        if current_date.isoweekday() == 2 or current_date.isoweekday() == 5:

            new_date = datetime.combine(current_date, nzne_dep_time)

            create_flight(dep_airport=df_airport, arr_airport=ci_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        # wednesday saturday
        if current_date.isoweekday() == 3 or current_date.isoweekday() == 6:

            new_date = datetime.combine(current_date, nzci_dep_time)

            create_flight(dep_airport=ci_airport, arr_airport=df_airport,
                          current_date=new_date, plane=plane, price=price,
                          flight_num=flight_num,
                          travel_mins=duration)

        current_date += day_delta


def create_nzne_to_nzro_to_yssy(start_date, end_date, df_airport):
    # once weekly
    # depart nzne friday
    # depart nzro friday
    # depart yssy sunday AEST

    nzne_dep_time = dt.time(6, 0, 0)
    nzro_dep_time = dt.time(7, 0, 0)
    yssy_dep_time = dt.time(12, 0, 0)

    plane = Plane.objects.get(plane_id="Hon002")

    ro_place = "NZRO"
    ro_airport = Airport.objects.get(airport_code=ro_place)

    sy_place = "YSSY"
    sy_airport = Airport.objects.get(airport_code=sy_place)

    # i dont understand pricing
    ne_sy_price = 900
    ro_sy_price = 800
    sy_ne_price = 1050

    flight_num = "DF27"

    ne_ro_duration = 40
    ro_sy_duration = 220
    sy_nz_duration = 200

    stop_mins = 20

    current_date = start_date
    day_delta = timedelta(days=1)

    while current_date < end_date:

        if current_date.isoweekday() == 5:

            first_date = datetime.combine(current_date, nzne_dep_time)
            second_date = datetime.combine(current_date, nzro_dep_time)

            # nzne to yssy - stop at nzro
            create_flight_with_stop(
                dep_airport=df_airport, stop_airport=ro_airport, arr_airport=sy_airport,
                first_departure_date=first_date, second_departure_date=second_date,
                first_leg_travel_mins=ne_ro_duration, second_leg_travel_mins=ro_sy_duration,
                stop_mins=stop_mins,
                plane=plane, price=ne_sy_price, flight_num=flight_num)

            # creates a flight for the second leg - uses second date

            create_flight(dep_airport=ro_airport, arr_airport=sy_airport,
                          current_date=second_date, plane=plane, price=ro_sy_price,
                          flight_num=flight_num,
                          travel_mins=ro_sy_duration)

        if current_date.isoweekday() == 7:

            # syd to nzne
            new_date = datetime.combine(current_date, yssy_dep_time)

            create_flight(dep_airport=sy_airport, arr_airport=df_airport,
                          current_date=new_date, plane=plane, price=sy_ne_price,
                          flight_num=flight_num,
                          travel_mins=sy_nz_duration)

        current_date += day_delta

