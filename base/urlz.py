from django.urls import path
from . import views

urlpatterns = [

    # AUTHENTICATION
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    # USER PROFILE
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),

    # HOME PAGE
    path('', views.home, name="home"),

    # OTHER PAGES
    path('about/', views.aboutPage, name="about"),
    path('gallery/', views.galleryPage, name="gallery"),
    path('services/', views.servicesPage, name="services"),
    path('contact/', views.contactPage, name="contact"),

    # CRUD - APPOINTMENT
    path('appointment/<str:pk>/', views.appointment, name="appointment"),
    path('create-appointment/', views.createAppointment, name="create-appointment"),
    path('view-appointment/', views.viewAppointment, name="view-appointment"),
    path('update-appointment/<str:pk>/', views.updateAppointment, name="update-appointment"),
    path('delete-appointment/<str:pk>/', views.deleteAppointment, name="delete-appointment"),

]
