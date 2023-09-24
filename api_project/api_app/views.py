from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .serializers import UserSerializer, ItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from functools import wraps
from .models import Item, Pedido

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(viewset, request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(viewset, request, *args, **kwargs)
        else:
            return Response({'error': 'Acesso negado. Somente superusuários podem acessar este recurso.'}, status=status.HTTP_403_FORBIDDEN)
    return _wrapped_view

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        Lista todos os Usuários.
        
        Parâmetros no body:
        - Nenhum.
        """
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Lista um Usuário em específico.
        
        Parâmetros no body:
        - Nenhum.
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    @superuser_required
    def create(self, request, *args, **kwargs):
        """
        Cria um novo Usuário.
        
        Somente para Usuários <b>SuperUser</b>.
        Parâmetros no body:
        - username: String, nome de usuário.
        - password: String, senha do usuário.
        - email: String, email do usuário.
        - first_name: String, primeiro nome do usuário.
        - last_name: String, último nome do usuário.
        - is_staff: String boolean ("True" ou "False"), determina se o Usuário pode acessar o /admin/.
        - is_superuser: String boolean ("True" ou "False"), determina se o Usuário tem acesso total ao sistema.
        - active: String boolean ("True" ou "False"), determina se o Usuário é ativo.
        """
        user_data = request.data.copy()
        user_data.setdefault('is_superuser', False)
        user_data.setdefault('is_staff', False)
        user_data.setdefault('is_active', True)

        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid():
            user = User.objects.create_user(**user_data)
            return Response({"username": user.username, "id": user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @superuser_required
    def partial_update(self, request, *args, **kwargs):
        """
        Edita informações do Usuário.

        Somente para Usuários <b>SuperUser</b>.
        Parâmetros no body:
        - Qualquer campo de Usuário inserido com um novo valor será alterado.
        - <b>Não irá alterar senha mesmo que seja enviada no body.</b>
        """
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
    

class ItemViewSet(viewsets.ViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        Lista todos os Itens.
        
        Parâmetros no body:
        - Nenhum.
        """
        queryset = Item.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Lista um Item em específico.
        
        Parâmetros no body:
        - Nenhum.
        """
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)
    
    @superuser_required
    def create(self, request):
        """
        Cria um novo Item.
        
        Somente para Usuários <b>SuperUser</b>.
        Parâmetros no body:
        - nome: String, nome do Item.
        - preco: Float, preço do item em Reais (Exemplo: 10.50).
        """
        item_data = request.data.copy()

        serializer = self.serializer_class(data=item_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @superuser_required
    def partial_update(self, request, *args, **kwargs):
        """
        Edita informações do item.

        Somente para Usuários <b>SuperUser</b>.
        Parâmetros no body:
        - Qualquer campo de Item inserido com um novo valor será alterado.
        """
        item_id = kwargs.get('pk')
        item = self.queryset.filter(pk=item_id).first()

        if not item:
            return Response({'error': 'Item não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @superuser_required
    def destroy(self, request, *args, **kwargs):
        """
        Remove definitivamente um Item.

        Somente para Usuários <b>SuperUser</b>.
        Aviso: Pedidos com este Item não serão afetados, porém haverá FKs para Itens não existentes.
        """
        item_id = kwargs.get('pk')
        queryset = Item.objects.all()
        item = queryset.filter(pk=item_id).first()

        if not item:
            return Response({'error': 'Item não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({'message': 'Item excluído com sucesso.'}, status=status.HTTP_200_OK)