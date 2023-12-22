from django.urls import path
from .views import *

urlpatterns = [
    path('hello/',HelloAPI.as_view(),name='hello'),
    path('translate/',TranslateDynamic.as_view(),name='translate'),
    path('translate/en-sr/',TranslateEN_SR.as_view(),name='en-sr'),
    path('translate/sr-en/',TranslateSR_EN.as_view(),name='sr-en'),
]