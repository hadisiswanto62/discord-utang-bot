from django.urls import path, include
from . import views

urlpatterns = [
    # this creates "login/" and "logout/"
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('user/', views.UserListView.as_view()),
    path('transaction/', views.TransactionListView.as_view()),
    path('transaction/<int:pk>/', views.TransactionDetailView.as_view()),
    path('transaction_group/', views.TransactionGroupListView.as_view()),
    path('transaction_group/<int:pk>/', views.TransactionGroupListView.as_view()),
    path('transaction_need_action/', views.TransactionNeedActionListView.as_view()),
]