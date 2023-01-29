from rest_framework import serializers
from .models import CustomUser
# use of Model Serializer to save time on setting password

from rest_framework import permissions

#custom permissions for project owner only to be able to edit
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: #is the logged in user the owner?
            return True
        return obj.owner == request.user #if it's true - the they should be able to edit 

class IsSupporterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.supporter == request.user

class IsOwnersProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        read_only_fields = ['id'] 
        extra_kwargs = {'password' : {'write_only' : True}}
    
    def create(self, validated_data):
        user = CustomUser (
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

