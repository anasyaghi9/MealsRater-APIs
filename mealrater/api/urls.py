from django.urls import path
from django.conf.urls import include
from .views import MealViewSet, RatingViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('meal', MealViewSet)
router.register('rating', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]