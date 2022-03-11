from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import GroupReadCompactSerializer
from .models import Group


# Create your views here.
class GroupsViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    action_serializers = {
        'list': GroupReadCompactSerializer
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
