from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import GroupReadCompactSerializer, RegisterSerializer, GroupCreateSerializer
from .models import Group
from rest_framework import generics
from rest_framework.response import Response
from .jwt import CustomTokenObtainPairSerializer
from rest_framework.mixins import CreateModelMixin
from .permissions import UserGroupPermissions
from rest_framework import status


# Create your views here.
class GroupsViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, UserGroupPermissions)
    queryset = Group.objects.all()
    action_serializers = {
        'list': GroupReadCompactSerializer,
        'create': GroupCreateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action)
        else:
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'groups': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'group': serializer.data, 'message': 'successfull'})

    def perform_create(self, serializer):
        instance = serializer.save()
        owner = self.request.user
        owner.group = instance
        owner.save()


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response({
            "token": str(CustomTokenObtainPairSerializer.get_token(user)),
            "message": "successful"
        })
