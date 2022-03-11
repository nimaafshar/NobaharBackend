from rest_framework.routers import SimpleRouter
from .jwt import EmailTokenObtainPairView
from .views import RegisterApi
from django.urls import path

router = SimpleRouter()

urlpatterns = [
                  path('auth/login/', EmailTokenObtainPairView.as_view()),
                  path('auth/signup/', RegisterApi.as_view())
              ] + router.urls
