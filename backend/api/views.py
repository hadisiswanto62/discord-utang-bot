from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from .serializers import UserSerializer
# Create your views here.
class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # def get(self, request, *args, **kwargs):
    #     users = User.objects.all()
    #     return Response(UserSerializer(users).data)