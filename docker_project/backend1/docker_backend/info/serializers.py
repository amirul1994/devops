from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'age', 'profession', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'age', 'profession', 'address']

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'age', 'profession', 'address']