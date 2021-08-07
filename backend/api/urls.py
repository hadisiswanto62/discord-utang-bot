from django.urls import path, include
from . import views

urlpatterns = [
    # this creates "login/" and "logout/"
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('user/', views.UserListView.as_view()),
]