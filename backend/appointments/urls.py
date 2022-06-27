
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('genrate/batch/', genrateBatches.as_view(),
         name='btch gnrt'),
    path('get/batch/<str:OFID>/', GetBatches.as_view(),
         name='btch get'),
    path('get/batch/timing/<str:BID>/', GetBatchesTimings.as_view(),
         name='btch timing get'),
     path('book/', createAppoin.as_view(),
         name='book api'),
]
