from rest_framework import serializers
from .models import Group, User


class GroupReadCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description')
        read_only_fields = ('id', 'name', 'description')


class GroupCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)
        extra_kwargs = {
            'name': {'write_only': True},
            'description': {'write_only': True},
        }

    def create(self, validated_data):
        return Group.objects.create(**validated_data, admin=self.context['request'].user)


class UserInGroupReadSerializer(serializers.ModelSerializer):
    rule = serializers.SerializerMethodField(method_name='is_owner')

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'rule')

    def is_owner(self, instance):
        if self.context['owner'].id == instance.id:
            return "Owner"
        else:
            return "Member"


class GroupReadDetailedSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(method_name='get_members')

    class Meta:
        model = Group
        fields = ('name', 'description', 'members')
        read_only_fields = ('name', 'description', 'members')

    def get_members(self, instance):
        serializer = UserInGroupReadSerializer(instance.members, context={'owner': instance.admin}, many=True)
        return serializer.data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['email'], name=validated_data['name'],
                                   email=validated_data['email'], password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
