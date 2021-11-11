from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Appointment, Department, User
from .forms import AppointmentForm, UserForm, MyUserCreationForm


# Create your views here.


def loginPage(request):
    page = 'login'

    # Hii ni kama mtu ka-login, apaswi kona login page unless ka-logout
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong! Try again later.')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    context = {}
    return render(request, 'base/home.html', context)


def appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    context = {'appointment': appointment}
    return render(request, 'base/appointment.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    appointments = user.appointment_set.all()

    context = {
        'user': user,
        'appointments': appointments,
    }
    return render(request, 'base/user_profile.html', context)


@login_required(login_url='/login')
def createAppointment(request):
    form = AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():

            # Hii mistari mitatu ni backend ielewe kuwa user = patient
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()

            return redirect('view-appointment')

    context = {'form': form}
    return render(request, 'base/form_appointment.html', context)


@login_required(login_url='/login')
def viewAppointment(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    appointments = Appointment.objects.filter(
        Q(dept__name__icontains=q) |
        Q(title__icontains=q) |
        Q(patient__username__icontains=q)
    )

    departments = Department.objects.all()
    appointment_count = appointments.count()

    context = {
        'appointments': appointments,
        'departments': departments,
        'appointment_count': appointment_count,
    }
    return render(request, 'base/view_appointment.html', context)


@login_required(login_url='/login')
def updateAppointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    form = AppointmentForm(instance=appointment)

    if request.user != appointment.patient:
        return HttpResponse("Access Denied!")

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('view-appointment')

    context = {'form': form}
    return render(request, 'base/form_appointment.html', context)


@login_required(login_url='/login')
def deleteAppointment(request, pk):
    appointment = Appointment.objects.get(id=pk)

    if request.user != appointment.patient:
        return HttpResponse("Access Denied!")

    if request.method == 'POST':
        appointment.delete()
        return redirect('view-appointment')
    return render(request, 'base/delete.html', {'obj': appointment})


@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', context)


def aboutPage(request):
    context = {}
    return render(request, 'base/about.html', context)


def galleryPage(request):
    context = {}
    return render(request, 'base/gallery.html', context)


def servicesPage(request):
    context = {}
    return render(request, 'base/services.html', context)


def contactPage(request):
    context = {}
    return render(request, 'base/contact.html', context)

