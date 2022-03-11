from rest_framework.routers import SimpleRouter
from .jwt import EmailTokenObtainPairView
from .views import RegisterApi
from django.urls import path
from .views import GroupsViewSet, JoinRequestsViewSet

router = SimpleRouter()
router.register('groups', GroupsViewSet, basename='groups')
router.register('join_requests', JoinRequestsViewSet, basename='join_requests')

urlpatterns = [
                  path('auth/login/', EmailTokenObtainPairView.as_view()),
                  path('auth/signup/', RegisterApi.as_view())
              ] + router.urls
