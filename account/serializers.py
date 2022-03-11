from rest_framework import serializers
from .models import Group


class GroupReadCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description')
        read_only_fields = ('id', 'name', 'description')
