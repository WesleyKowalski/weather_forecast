---
Para executar o projeto deve ser seguido os seguintes passos abaixo
Criar um env para o python=3, usando o comando abaixo:
---
python3 -m venv env
---

Após isso executar o env, usando o comando abaixo:
---
source env/bin/activate
---

Agora deverá ser instalado os requerimentos da aplicação, dentro do env que está sendo executado.
Para instalar os requerimentos deverá usar os seguintes comandos:
---
pip install wheel
pip install -r requirements.txt
---

--------------------------------------------------------------------------------------------------------------
INICIO - PASSO_ESPECIFICO_DE_GERACAO_DE_TOKEN
---
OBS: Esses passos não precisam ser executados caso já exista uma base de dados e também um usuário criado
--------------------------------------------------------------------------------------------------------------

Deverá ser criado a base de dados local, para isso deverá ser utilizado o comando
---
python3 manage.py migrate
---

Após isso precisamos criar um usuário para autenticar as requisições
---
python3 manage.py shell
---

Dentro do shell da aplicação vai ser criado primeiramente um usuário, e depois um token para o mesmo,
O que deverá ser informado nos pamâmetros:
    --> Nome_usuario_desejado = Nome de usuário que for da sua escolha, sem espaços.
    --> Senha_usuario_desejado = Senha de usuário que for da sua escolha.
---
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.create_user(username='Nome_usuario_desejado', password='Senha_usuario_desejado', is_superuser=True, is_staff=True)
token = Token.objects.create(user=user)
token.key
---

Depois de feito esse procedimento o usuário já estará criado, e o token já vai estar disponivel para utilização.
--------------------------------------------------------------------------------------------------------------
FIM - ESSES PASSO NÃO PRECISA SER EXECUTADO CASO JÁ EXISTA UMA BASE DE DADOS E TAMBÉM UM USUÁRIO CRIADO
--------------------------------------------------------------------------------------------------------------

Após isso a aplicação pode ser executada com o seguinte comando:
---
python3 manage.py runserver
---

Requisições na aplicação
--
 --> O header de requisição é: "Token GERADO_NO_PASSO_ESPECIFICO_DE_GERACAO_DE_TOKEN"

     --> Os endPoint's que podem ser consultados são:
        "URL_INICIAL/api/v1/forecastforcity"
        "URL_INICIAL/api/v1/alllog"

  --> A URL inicial é definida na hora de executar o projeto(python3 manage.py runserver),
      a partir daquela URL deverá ser acrescentado os endPoints.

 --> Vamos seguir com o exemplo como se a URL_INICIAL fosse  http://127.0.0.1:8000

 --> Especificações de endPoint's e parâmetros:

    --> "http://127.0.0.1:8000/api/v1/forecastforcity"

        --> Parâmetros:
            --> city = Cidade de busca desejada

        --> Exemplo de uso:
            http://127.0.0.1/api/v1/forecastforcity?city=Blumenau

    --> "http://localhost:8000/api/v1/alllog"
        --> Parâmetros:
            --> date_min_log = data mínima para busca do log
                --> Exemplo de formatação:
                    2021-12-15 00:01:00
            --> date_min_max = data máxima para busca do log
                --> Exemplo de formatação:
                    2021-12-15 23:59:01

        --> Exemplo de uso:
            http://127.0.0.1:8000/api/v1/alllog?data_log_min=2021-12-14 00:01:01&data_log_max=2021-12-15 09:19:01