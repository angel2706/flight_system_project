from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=True, unique=True)
    fname = models.CharField(max_length=50, null=True)
    lname = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return str(self.username)