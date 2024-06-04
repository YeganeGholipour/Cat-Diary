from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CatDiary
from .serializers import CatSerializer, RegisterSerializer
from django.contrib.auth.models import User

from datetime import datetime



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

    def get(self, request):
        cats = CatDiary.objects.filter(user=request.user.id)
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DiaryEntryByDate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, date):
        date_str = request.query_params.get('date', None)

        if not date_str:
            return Response({'date': 'This date is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'date': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

        diary_entry = CatDiary.objects.filter(user=request.user.id, date=date)
        if not diary_entry:
            return Response({'diary_entry': 'No diary entry found for this date.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CatSerializer(diary_entry, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
