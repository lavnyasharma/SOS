
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('login/doctor/', RegisterAsDoctorView.as_view(),
         name='doctor regestration'),
    path('doctor/specialization/', SpecializationView.as_view(),
         name='Specialization regestration'),
    path('doctor/specialization/<str:speid>/', SpecializationInstanceView.as_view(),
         name='Specialization regestration instance'),
    path('doctor/specialization/add/<str:speid>/', doc_specializationView.as_view(),
         name='Specialization add'),
    path('doctor/hospital/', HospitalView.as_view(),
         name='hospital add'),
    path('doctor/office/', OfficeView.as_view(),
         name='office'),
    path('doctor/office/<str:id>/', OfficeInstanceView.as_view(),
         name='office instance'),
    path('add/doctor/', DoctorView.as_view(), name='doctor add'),
    path('doctor/qualification/', QualiView.as_view(),
         name='qualification'),
     path('doc/', getAllDoctorData.as_view(),name='all doctor data'),
]
