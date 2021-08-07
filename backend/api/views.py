from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel, Transaction, TransactionGroup
from .serializers import UserSerializer, TransactionGroupSerializer, TransactionSerializer
class UserListView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class TransactionListView(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        queryset = Transaction.objects.all()
        sender_id = self.request.query_params.get("sender", None)
        if sender_id != None:
            queryset = queryset.filter(sender__id=int(sender_id))

        receiver_id = self.request.query_params.get("receiver", None)
        if receiver_id != None:
            queryset = queryset.filter(receiver__id=int(receiver_id))

        is_paid = self.request.query_params.get("is_paid", None)
        if is_paid != None:
            val = None
            if is_paid.lower()=="true":
                val = True
            elif is_paid.lower()=="false":
                val = False
            else:
                return Response({"msg": f"Invalid parameter for `is_paid`: {is_paid}"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(is_paid=val)

        mode = self.request.query_params.get("mode", None)
        if mode == "sender":
            if sender_id == None:
                return Response({"msg": f"Missing parameter `sender`"}, status=status.HTTP_400_BAD_REQUEST)
            if int(sender_id) != self.request.user.id:
                return Response({"msg": f"Cannot get Transactions with sender={sender_id} : Not Authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
        elif mode == "receiver":
            if receiver_id == None:
                return Response({"msg": f"Missing parameter `receiver`"}, status=status.HTTP_400_BAD_REQUEST)
            if int(receiver_id) != self.request.user.id:
                return Response({"msg": f"Cannot get Transactions with receiver={receiver_id} : Not Authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"msg": "Missing parameter `mode`"}, status=status.HTTP_400_BAD_REQUEST)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionGroupListView(ListCreateAPIView):
    queryset = TransactionGroup.objects.all()
    serializer_class = TransactionGroupSerializer

class TransactionGroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TransactionGroup.objects.all()
    serializer_class = TransactionGroupSerializer

    
class TransactionNeedActionListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(sender__id=self.request.user.id, is_paid=False)