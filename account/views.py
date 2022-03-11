from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import GroupReadCompactSerializer, RegisterSerializer, GroupCreateSerializer, \
    GroupReadDetailedSerializer, JoinRequestReadSerializer
from .models import Group, JoinRequest
from rest_framework import generics
from rest_framework.response import Response
from .jwt import CustomTokenObtainPairSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from .permissions import UserGroupPermissions, UserJoinRequestPermissions
from rest_framework.decorators import action
from rest_framework import status


# Create your views here.
class GroupsViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, UserGroupPermissions)
    queryset = Group.objects.all()
    action_serializers = {
        'list': GroupReadCompactSerializer,
        'create': GroupCreateSerializer,
        'my_group': GroupReadDetailedSerializer
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

    @action(detail=False, url_path='my', url_name='my_group', methods=['GET'])
    def my_group(self, request):
        instance = request.user.group
        serializer = self.get_serializer(instance)
        return Response({'group': serializer.data})


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


class JoinRequestsViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, UserJoinRequestPermissions)
    action_serializers = {
        'list': JoinRequestReadSerializer,
        'group_requests': JoinRequestReadSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action)
        else:
            return None

    def list(self, request, *args, **kwargs):
        queryset = request.user.join_requests
        serializer = self.get_serializer(queryset, many=True)
        return Response({'joinRequests': serializer.data})

    @action(detail=False, url_path='group', url_name='group_requests', methods=['GET'])
    def group_requests(self, request):
        queryset = request.user.group.join_requests
        serializer = self.get_serializer(queryset, many=True)
        return Response({'joinRequests': serializer.data})
