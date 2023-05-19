from django.urls import path
from .views import *


urlpatterns = [
    path('guest/sos/',
         sosView.as_view(), name='guest sos'),
     path('logged/sos/',
         LoggedSosView.as_view(), name='logged sos'),
         path('guest/get/',
         sosgetView.as_view(), name='guest sos'),
         path('guest/all/',
         sosgetallView.as_view(), name='guest sos'),
   
    path('guest/cood/',
         updateView.as_view(), name='guest sos cood update'),
    path('freeway/',
         freeView.as_view(), name='guest sos cood update')
]
