from django.contrib import admin

# Register your models here.

from .models import Appointment, Department, Doctor, User

admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(Department)
admin.site.register(Doctor)
