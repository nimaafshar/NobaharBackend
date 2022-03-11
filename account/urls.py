from rest_framework.routers import SimpleRouter
from .jwt import EmailTokenObtainPairView
from django.urls import path

router = SimpleRouter()

urlpatterns = [
                  path('auth/login/', EmailTokenObtainPairView.as_view())
              ] + router.urls
