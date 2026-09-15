from rest_framework import viewsets
from .serializers import RatingSerializer, MealSerializer, UserSerializer
from .models import Meal, Rating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # #authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                'token': token.key, 
                }, 
            status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' not in request.data:
            return Response(
                {'message': 'stars not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stars = request.data['stars']
        user = request.user


        try:
            meal = Meal.objects.get(id=pk)
        except Meal.DoesNotExist:
            return Response(
                {'message': 'Meal not found'},
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

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        return Response(
            {'message': 'Not Allowed To Update!'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'message': 'Not Allowed To Update!'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    def create(self, request, *args, **kwargs):
        return Response(
            {'message': 'Not Allowed To Create!'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    