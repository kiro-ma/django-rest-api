from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .serializers import PedidoSerializer, UserSerializer, ItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from functools import wraps
from .models import Item, Pedido, PedidoItem
from django.utils import timezone

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
        - username (String): Nome de usuário.
        - password (String): Senha do usuário.
        - email (String): Email do usuário.
        - first_name (String): Primeiro nome do usuário.
        - last_name (String): Último nome do usuário.
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
        
    @superuser_required
    def get_by_username(self, request, username=None):
        """
        Busca Usuário por username.
        
        Somente para Usuários <b>SuperUser</b>.
        Parâmetros na URL:
        - username (String): Nome de usuário.
        """
        queryset = User.objects.filter(username=username)
        if queryset:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        """
        Muda a senha de um Usuário.

        Parâmetros no body:
        - current_password (String): Senha atual.
        - new_password (String): Nova senha.
        """
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
    
    def list_by_nome(self, request, nome_str=None):
        """
        Lista o Item de acordo com seu nome.

        Parâmetros na URL:
        - String ou substring, nome do Item.
        """
        queryset = Item.objects.filter(nome__icontains=nome_str)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    @superuser_required
    def create(self, request):
        """
        Cria um novo Item.
        
        Somente para Usuários <b>SuperUser</b>.
        Parâmetros no body:
        - nome (String): Nome do Item.
        - preco (Float): Preço do item em Reais (Exemplo: 10.50).
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
        Aviso: Pedidos com este Item o perderão da lista de itens.
        """
        item_id = kwargs.get('pk')
        queryset = Item.objects.all()
        item = queryset.filter(pk=item_id).first()

        if not item:
            return Response({'error': 'Item não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({'message': 'Item excluído com sucesso.'}, status=status.HTTP_200_OK)
    

class PedidoViewSet(viewsets.ViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        Lista todos os Pedidos.
        
        Parâmetros no body:
        - Nenhum.
        """
        queryset = Pedido.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def list_by_data(self, request, user_id=None):
        """
        Lista todos os Pedidos em um intervalo de datas.
        Este é um endpoint especial, se colocar "username" na URL, além de filtrar por data também vai filtrar pelo User.
        Mas se deixar somente com as datas, irá filtrar os Pedidos de todos os Users por data.

        Parâmetros na URL:
        - data_inicial, formato YYYY-MM-DD.
        - data_final, formato YYYY-MM-DD.
        - username, nome de usuário.
        """
        data_inicial = request.query_params.get('data_inicial', None)
        data_final = request.query_params.get('data_final', None)
        username = request.query_params.get('username', None)

        if not data_inicial or not data_final:
            return Response({'error': 'Intervalo de datas impossivel.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_inicial = timezone.datetime.strptime(data_inicial, '%Y-%m-%d')
            data_final = timezone.datetime.strptime(data_final, '%Y-%m-%d')

            if data_inicial > data_final:
                return Response({'error': 'Data inicial maior do que data final.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if username:
                queryset = Pedido.objects.filter(data_criacao__gte=data_inicial, data_criacao__lte=data_final, user=User.objects.get(username=username))
            else:
                queryset = Pedido.objects.filter(data_criacao__gte=data_inicial, data_criacao__lte=data_final)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Erro ao procurar Pedidos, ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Lista um Pedido em específico.
        
        Parâmetros no body:
        - Nenhum.
        """
        queryset = Pedido.objects.all()
        pedido = get_object_or_404(queryset, pk=pk)

        pedido_itens = pedido.itens.all()

        data = {
            'id': pedido.id,
            'user': pedido.user.id,
            'itens': [{'id': item.id, 'nome': item.nome, 'preco': item.preco} for item in pedido_itens]
        }

        return Response(data, status=status.HTTP_200_OK)
    
    @superuser_required
    def create(self, request, *args, **kwargs):
        """
        Cria um novo Pedido.

        Crie um novo pedido para um usuário com uma lista de itens e quantidades associadas.

        Parâmetros no body:
        - user (int): ID do usuário que está fazendo o pedido.
        - itens (list of int): Uma lista de IDs de itens que serão incluídos no pedido.
        - quant (list of int): Uma lista de quantidades correspondentes aos itens. 
          Os índices nas listas 'itens' e 'quant' devem corresponder aos mesmos itens.
          Exemplo:
          - Se 'itens' for [1, 2, 5] e 'quant' for [3, 2, 5], os itens no pedido serão:
            - Item 1: 3 unidades.
            - Item 2: 2 unidades.
            - Item 5: 5 unidades.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()
            pedido_query = Pedido.objects.get(pk=pedido.id)
            pedido_data = request.data.copy()

            for item_id, quant in zip(pedido_data["itens"], pedido_data["quant"]):
                PedidoItem.objects.create(pedido=pedido_query, item=Item.objects.get(pk=item_id), quantidade=quant).save()

            return Response({'message': 'Pedido criado com sucesso.', 'id': pedido.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list_by_user(self, request, user_id=None):
        """
        Lista os Pedidos de um usuário específico.

        Parâmetros na URL:
        - user_id: ID do usuário a ser pesquisado.
        """
        queryset = Pedido.objects.filter(user_id=user_id)
        if queryset:
            serializer = self.serializer_class(queryset, many=True)
        else:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nenhum pedido encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
    @superuser_required
    def partial_update(self, request, *args, **kwargs):
        """
        Edita informações do Pedido.

        Somente para Usuários <b>SuperUser</b>.
        Parâmetros no body:
        - status_pagamento, String boolean ("True" ou "False"), determina o status do pagamento.
        - cancelado, String boolean ("True" ou "False"), determina o status do pedido.
        """
        pedido_id = kwargs.get('pk')
        pedido = self.queryset.filter(pk=pedido_id).first()

        pedido_data = request.data.copy()
        pedido_data.setdefault('status_pagamento', False)
        pedido_data.setdefault('cancelado', False)

        if not pedido:
            return Response({'error': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if 'status_pagamento' in request.data:
            pedido.status_pagamento = request.data['status_pagamento']
        if 'cancelado' in request.data:
            pedido.cancelado = request.data['cancelado']

        pedido.save()

        serializer = self.serializer_class(pedido)

        return Response(serializer.data, status=status.HTTP_200_OK)
