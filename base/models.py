from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.IntegerField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    title = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.IntegerField()
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Hii ni kwaajili ya ku-order (ascending or descending) appointments
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
