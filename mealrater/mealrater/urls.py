from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken.views import ObtainAuthToken 


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('tokenrequest/', ObtainAuthToken.as_view()),
]
