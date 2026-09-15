from django.urls import path
from django.conf.urls import include
from .views import MealViewSet, RatingViewSet, UserViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('meal', MealViewSet)
router.register('rating', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]