from rest_framework.generics import ListCreateAPIView
from .models import UserModel
from .serializers import UserSerializer
class UserListView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer