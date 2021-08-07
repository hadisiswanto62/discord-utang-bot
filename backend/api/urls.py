from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserListView.as_view({'get': 'list', 'post': 'create'})),
]