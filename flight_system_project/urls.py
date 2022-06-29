"""flight_system_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from users import views as user_views
from flights import views as flight_views
from booking import views as booking_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', user_views.register_user, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('search/', flight_views.search, name='search'),
    path('', flight_views.search, name='search'),
    path('results/', flight_views.results, name='results'),

    # path('create/', flight_views.create_new_flight, name='create'),
    # path('create-nonstop/', flight_views.create_nonstop, name='create-nonstop'),
    # path('create-multi/', flight_views.create_multi, name='create-multi'),
    #
    # path('created-nonstop/', flight_views.create_nonstop_results, name='created-nonstop'),
    # path('created-multi/', flight_views.create_multi_results, name='created-multi'),

    path('populate-flights/', flight_views.populate_data, name="populate-flights"),
    path('populate-base/', flight_views.populate_base_data, name="populate-base"),

    path('book-flight/', booking_views.book_flight, name="book-flight"),
    path('create-booking-invoice/', booking_views.create_booking_invoice, name="create-booking-invoice"),
    path('view-booking-invoice/', booking_views.view_booking_invoice, name="view-booking-invoice"),
    path('view-bookings/', booking_views.view_bookings, name="view-bookings"),
    path('cancelled-booking/', booking_views.cancelled_booking , name="cancelled-booking")
]
