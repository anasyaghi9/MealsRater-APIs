from rest_framework import viewsets
from .serializer import RatingSerializer, MealSerializer
from .models import Meal, Rating

class MealviewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class RatingviewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
