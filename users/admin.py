from django.contrib import admin
from .models import Customer

# Register your models here.
user_models = [Customer]

admin.site.register(user_models)