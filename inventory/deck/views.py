from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .serializers import UserSerializer

from django.contrib.auth import authenticate

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class ItemViewSet(LoginView, viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()

    def retrieve(self, request, pk=None):
        item = cache.get(f'item_{pk}')
        if not item:
            try:
                item = Item.objects.get(pk=pk)
                cache.set(f'item_{pk}', item, timeout=60*15)  # Cache for 15 minutes
            except Item.DoesNotExist:
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        item = self.get_object()
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class RegisterView(LoginView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

