from rest_framework import serializers
from .models import CatDiary
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user



class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatDiary
        fields = ['date', 'entry', 'photo']

    def create(self, validated_data):
        user = self.context['request'].user
        return CatDiary.objects.create(user=user, **validated_data)
