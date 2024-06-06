from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.cache import cache

from .models import CatDiary
from .serializers import CatSerializer, RegisterSerializer
from django.contrib.auth.models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListDiary(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        cache_key = f'cats_{request.user.id}'
        cats = cache.get(cache_key)

        if not cats:
            cats = CatDiary.objects.filter(user=request.user)
            serializer = CatSerializer(cats, many=True)
            cats_data = serializer.data
            cache.set(cache_key, cats_data, 60 * 60 * 24)
        else:
            # Deserialize cached data
            serializer = CatSerializer(data=cats, many=True)
            serializer.is_valid()  # Check if the data is valid
            cats_data = serializer.data

        return Response(cats_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Invalidate the cache for this user
            cache.delete(f'cats_{request.user.id}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DiaryEntryByDate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date', None)

        if not date_str:
            return Response({'date': 'This date is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'date': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'diary_entry_{request.user.id}_{date_str}'
        diary_entry = cache.get(cache_key)

        if not diary_entry:
            diary_entry = CatDiary.objects.filter(user=request.user, date=date)
            if not diary_entry.exists():
                return Response({'diary_entry': 'No diary entry found for this date.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CatSerializer(diary_entry, many=True)
            cache.set(cache_key, serializer.data, 60 * 60 * 24)
        else:
            # Deserialize cached data
            diary_entry = CatSerializer(data=diary_entry, many=True)
            diary_entry.is_valid()

        return Response(diary_entry.data, status=status.HTTP_200_OK)
