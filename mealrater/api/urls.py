from django.urls import path
from django.conf.urls import include
from .views import MealviewSet, RatingviewSet
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('meal', MealviewSet)
routers.register('rating', RatingviewSet)

urlpatterns = [
    path('', include(routers.urls)),
]