from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer