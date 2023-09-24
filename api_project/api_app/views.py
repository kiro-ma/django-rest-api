from django.shortcuts import render
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user_data = request.data.copy()
        user_data.setdefault('is_superuser', False)
        user_data.setdefault('is_staff', False)
        user_data.setdefault('is_active', True)

        serializer = self.get_serializer(data=user_data)

        if serializer.is_valid():
            user = User.objects.create_user(**user_data)
            return Response({"username": user.username, "id": user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # Verifique se a senha atual está correta
        if not user.check_password(current_password):
            return Response({'error': 'Senha atual incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

        # Atualize a senha do usuário para a nova senha
        user.password = make_password(new_password)
        user.save()

        return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)