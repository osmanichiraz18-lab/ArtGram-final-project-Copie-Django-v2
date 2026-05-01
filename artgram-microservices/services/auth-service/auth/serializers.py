from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, UserRole

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """User serializer for profile management"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'bio', 'profile_picture', 'date_of_birth', 'created_at', 
                  'is_staff', 'is_active']
        read_only_fields = ['id', 'created_at', 'is_staff']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class RoleSerializer(serializers.ModelSerializer):
    """Role serializer"""
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserRoleSerializer(serializers.ModelSerializer):
    """User role assignment serializer"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'assigned_at', 'assigned_by', 
                  'role_name', 'user_username']
        read_only_fields = ['id', 'assigned_at', 'assigned_by']
