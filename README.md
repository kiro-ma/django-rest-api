
# API Django RESTful

A API oferece um sistema de gerenciamento de usuários, itens e pedidos. É possível, autenticar e atualizar informações de perfil de usuários. Além disso, é possível adicionar novos itens, atualizar seus detalhes e excluir itens existentes. O destaque da API é a capacidade de criar e rastrear pedidos personalizados, que podem incluir uma variedade de itens e quantidades. Com recursos de autenticação e autorização, garantindo controle total sobre quem pode acessar e gerenciar esses recursos.


## Rodando localmente

Clone o projeto
```bash
  git clone https://github.com/kiro-ma/django-rest-api.git
```
Entre no diretório do projeto
```cmd
  cd django-rest-api
```
Crie um ambiente virtual Python versão 3.10.11, e o ative.

Crie um arquivo chamado .env com as seguintes variáveis:
```
DB_NAME=*nome do banco Postgres*
DB_USER=*usuario postgres*
DB_PASSWORD=*senha*
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=*chave secreta django*
DEBUG=True
```
Com o ambiente virtual ativado, execute o comando:
```cmd
pip install -r requirements.txt
```
Crie um banco de dados Postgres com o mesmo nome da variável DB_NAME do .env.

Entre no diretório do manage.py
```
cd api_project
```
Atualize o banco de dados com os comandos:
```
python manage.py makemigrations
```
e
```
python manage.py migrate
```
Inicie a aplicação:
```
python manage.py runserver
```




## Documentação

Após rodar o sistema no localhost:8000, acesse /docs/.
[Documentação Swagger](http://127.0.0.1:8000/docs/)

#### O sistema também está inteiramente documentado no django admin:
[Página de Admin](http://127.0.0.1:8000/admin/)

## Resumo de Funcionalidades

### Token JWT
A API possui autenticação por JSON Web Token, utilize os endpoints de Token listados na [documentação](http://127.0.0.1:8000/docs/) para receber tokens Access e Refresh, o token de acesso deve ser colocado no header das requisições, todas as requisições estão em um arquivo .json na raiz do repositório, utilize esse arquivo para importar todos os exemplos de requisições possíveis no app Insomnia.

### Item:
- Listar todos os Itens.
- Criar um novo item.
- Listar Itens pesquisando pelo nome.
- Listar um Item específico, por ID.
- Editar dados de um Item.
- Remover definitivamente um item.

Obs: Itens possuem quantidade de estoque, que será utilizada para fazer verificações nas quantidades de itens nos Pedidos.

### Pedido
- Listar todos os Pedidos.
- Criar um novo Pedido.
- Listar Pedidos em um intervalo de datas, com opção de filtrar por Usuário.
- Listar Pedidos de um Usuário específico, por ID.
- Listar um Pedido específico pro ID.
- Editar dados de um Pedido.

Em um determinado Pedido podem haver diferentes Itens cada um com suas quantidades, se disponível no estoque, por exemplo, um Pedido pode conter 5 Itens A e 1 Item B.

### User
- Listar todos os Usuários.
- Criar um novo Usuário.
- Buscar Usuário por username.
- Buscar um Usuário específico por ID.
- Editar os dados de um Usuário (não altera senha nem username).
- Mudar a senha do Usuário.

