from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=12)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    @staticmethod
    def validate_password(value):
        if len(value) < 12:
            raise serializers.ValidationError("Password must be at least 12 characters long.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Todo
        fields = '__all__'
