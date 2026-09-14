from rest_framework import viewsets
from .serializers import RatingSerializer, MealSerializer
from .models import Meal, Rating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' not in request.data:
            return Response(
                {'message': 'stars not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if 'username' not in request.data:
            return Response(
                {'message': 'username not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stars = request.data['stars']
        username = request.data['username']

        try:
            meal = Meal.objects.get(id=pk)
        except Meal.DoesNotExist:
            return Response(
                {'message': 'Meal not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'message': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # update
            rating = Rating.objects.get(user=user, meal=meal)
            rating.stars = stars
            rating.full_clean()
            rating.save()
            serializer = RatingSerializer(rating, many=False)
            return Response(
                {'message': 'Meal Rate Updated', 'result': serializer.data},
                status=status.HTTP_200_OK
            )

        except Rating.DoesNotExist:
            # create if the rating doesn't exist
            try:
                rating = Rating(stars=stars, meal=meal, user=user)
                rating.full_clean()
                rating.save()
            except ValidationError as e:
                return Response(
                    {'message': 'Invalid data', 'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RatingSerializer(rating, many=False)
            return Response(
                {'message': 'Meal Rate Created', 'result': serializer.data},
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response(
                {'message': 'Invalid data', 'errors': e.message_dict},
                status=status.HTTP_400_BAD_REQUEST
            )


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer