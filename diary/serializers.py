# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CatDiary

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
        user.save()
        return user





class CatSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)

    class Meta:
        model = CatDiary
        fields = ['date', 'entry', 'photo']

    def create(self, validated_data):
        user = self.context['request'].user
        photo = validated_data.get('photo')
        diary_entry = CatDiary.objects.create(
            user=user,
            date=validated_data['date'],
            entry=validated_data['entry'],
            photo=photo
        )
        diary_entry.save()
        return diary_entry

