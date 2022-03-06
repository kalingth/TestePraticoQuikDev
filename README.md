<p align="center">
    <a href="https://quikdev.com.br/">
        <img height="50px" src="Testes/EndpointTests/QuikDevLogo.png"/>
    </a>
</p>

# Teste Prático QuikDev

## Introdução

> Este teste busca identificar diferentes níveis de habilidade, medindo conhecimento,
organização e esforço.
> <p align="right"><a href="https://quikdev.com.br/">QuikDev</a></p>

<p>&nbsp;&nbsp;&nbsp;&nbsp;Teste prático realizado para avaliação
das minhas competências como desenvolvedor Back-end.</p>

---

### &nbsp;&nbsp;&nbsp;&nbsp;A implementação das seguintes features eram essenciais para esse projeto e foram alcançadas:


1. Elaborar um arquivo de Markdown para o projeto com
informações da stack utilizada;<br>


2. Criação da estrutura base de armazenamento dos dados
seguindo o padrão descrito no documento encaminhado;<br>


3. Criar um sistema de autenticação por tokens para a
API desenvolvida;<br>


4. Criação de endpoints para manipulação dos dados do usuário
baseados nas operações **CRUD**; 
   1. Esse endpoint deverá ter um controle de acesso.


5. Criação de endpoints para manipulação das postagens dos
usuários baseados nas operações **CRUD**;<br>
   1. Apenas o dono da postagem poderá editar ou excluir as postagens;
   2. postagem deve possuir um endpoint dedicado à inserção de imagens.


6. Criação de endpoints para manipulação dos comentários dos
usuários nas postagens baseados nas operações **CRUD**;<br>
    1. Apenas o dono do comentário poderá realizar sua edição;
    2. O dono do comentário deve poder remover o comentário;
    3. O dono da postagem também deverá poder remover o comentário.


7. Criar um endpoint que gere um relatório que traga as seguintes
informações sobre as postagens:
    1. Título;
    2. Quantidade de comentários realizados.

---

### &nbsp;&nbsp;&nbsp;&nbsp;As seguintes features não eram obrigatórias, porém foram desenvolvidas:

1. Sistema de notificação por email para informar o usuário que há
um novo comentário em sua postagem;
2. Documentação da aplicação utilizando o postman. Podendo ser
acessada através do seguinte anchor: [Documentação Postman](https://documenter.getpostman.com/view/14436122/UVkvKYQf);
3. Realização de teste de cada um dos endpoints desenvolvidos.

<br>

> <p align="justify"><b>Considerações</b>: Não foram desenvolvidas as demais features para
> nível sênior não por estar participando do processo para desenvolvedor
> pleno, mas porque considerei o desenvolvimento de testes de integração
> de grande importância e estes testes acabam levando bastante tempo para
> serem desenvolvidos.</p>

## Endpoints

Rotas dos endpoints da API desenvolvida:

```
root
│   
└───/auth
│   │   POST - Realizar login.
│
└───/users
│   │   POST - Criar Usuário.
│   │   GET - Recuperar todos os usuários. (apenas administradores)
│   │
│   └───/id
│       │   GET - Recuperar dados do usuário.
│       │   PUT - Atualizar dados do usuário em lote.
│       │   PATCH - Atualizar dados do usuário individualmente.
│       │   DELETE - Deletar os dados do usuário do sistema.
│
└───/posts
│   │   POST - Criar nova postagem.
│   │
│   └───/id
│       │   GET - Recuperar dados da postagem.
│       │   PUT - Atualizar dados da postagem em lote.
│       │   PATCH - Atualizar da postagem individualmente.
│       │   DELETE - Deletar a postagem do sistema.
│       │
│       └───/images
│       │   │   POST - Inserir imagens em uma postagem.
│       │   │   GET  - Recuperar todas as imagens de uma postagem.
│       │   │
│       │   └───/id
│       │       │   DELETE - Deletar uma imagem da postagem.
│       │
│       └───/comments
│           │   POST - Inserir um novo comentário em uma postagem.
│           │   GET - Recuperar todos os comentários de uma postagem.
│           │
│           └───/id
│               │   GET - Recuperar um comentário de uma postagem.
│               │   PUT - Alterar um comentário de uma postagem.
│               │   PATCH - Alterar um comentário de uma postagem.
│               │   DELETE - Deletar um comentário de uma postagem.
│
└───/summary
│   │   GET - Recuperar um resumo da utilização da plataforma.

```

## Stack

- **Linguagem**: Python
- **Versão**: 3.9.7
- **Banco de Dados**: SQLite3
- **Bibliotecas**:
  - **Flask**: Microframework de poderoso para desenvolvimento de APIs em **Python**;
  - **SQLAlchemy**: Biblioteca para auxiliar na manipulação dos bancos de dados;
  - **MarshMallow**: Biblioteca responsável por facilitar a transformação de dados em dicionários a serem consumidos;
  - **PyJWT**: Biblioteca responsável por criar e processar o JSON Object Token - o token de autenticação utilizado para este projeto;
  - **Mailjet**: Biblioteca responsável por servir com um endpoint utilizando os servidores da MailJet para envio de emails;
  - **Requests**: Biblioteca utilizada para o desenvolvimento dos testes de integração do projeto;
  - **Sqlite3**: Por se tratar de um projeto não oficial, foi empregada a utilização do SQLite3 para facilitar a utilização deste projeto sem ter de instalar nada além das bibliotecas e do Python3.8+;

## Utilização

> **Nota**: É estritamente necessária a utilização da versão 3.8+ do Python. Recursos como a função **Walrus** foram empregados no desenvolvimento deste código.

&nbsp;&nbsp;&nbsp;&nbsp;A primeira coisa a fazer é instalar as bibliotecas utilizadas pela aplicação.
As biblioteca podem ser instaladas através do seguinte comando através do **Terminal**/**Prompt**/**Shell**:

```console
wall@kalingth:~$ pip install -r requeriments.txt
```

&nbsp;&nbsp;&nbsp;&nbsp;Ao fim da instalação das dependencias, basta rodar o seguinte comando ***python main.py*** e você terá um retorno parecido com esse:
```console
wall@kalingth:~$ python main.py
* Serving Flask app 'APP' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on all addresses.
  WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

&nbsp;&nbsp;&nbsp;&nbsp;Neste momento o próprio servidor criará as dependencias necessárias para o seu correto funcionamento.<br>

&nbsp;&nbsp;&nbsp;&nbsp;Para utilizar os testes desenvolvidos, basta acessar a pasta ***Testes*** através de outro **Terminal**/**Prompt**/**Shell** e rodar o comando ***py TestesEmLote.py*** e você obterá um retorno parecido com esse:

> **Nota**: É extremamente importante que modifique pelo menos o email do usuário 1 do arquivo de testes para que seja testado o recebimento do email.

```console
wall@kalingth:~$ py TestesEmLote.py

Rotina de Criação de Usuário e Login
------------------------------------------------------------------------------------------------------
Criando os Usuários e testando a realização de Login...                                             Ok
Tentando criar um usuário com um email que já existe...                                             Ok
Tentando acessar uma conta inexistente...                                                           Ok
Tentando acessar uma conta com a senha incorreta...                                                 Ok

Rotina de Leitura de Usuários
------------------------------------------------------------------------------------------------------
Recuperando os dados do primeiro usuário com suas credenciais...                                    Ok
Tentando recuperar dados do segundo usuário com as credenciais do primeiro...                       Ok
Tentando recuperar dados de usuários com um usuário não autenticado...                              Ok

Rotina de Edição de Dados de Usuários
------------------------------------------------------------------------------------------------------
Alterando, com PUT, os dados do primeiro usuário com suas credenciais...                            Ok
Alterando, com PATCH, os dados do primeiro usuário com suas credenciais...                          Ok
Tentando alterar, com PATCH, o escopo da conta do usuário com suas credenciais...                   Ok
Tentando alterar dados do segundo usuário com as credenciais do primeiro...                         Ok

Rotina de Criação de Postagens
------------------------------------------------------------------------------------------------------
Criando postagens como o Usuário 1...                                                               Ok
Tentando criar postagens como o Usuário 1 com uma requisição incompleta...                          Ok
Tentando criar postagens como o Usuário 2...                                                        Ok

Rotina de Leitura de Postagens
------------------------------------------------------------------------------------------------------
Recuperando a primeira postagem do Usuário 1 com suas credenciais...                                Ok
Recuperando a primeira postagem do Usuário 1 com as credenciais do Usuário 2...                     Ok
Tentando recuperar postagens com um usuário não autenticado...                                      Ok

Rotina de Edição de Postagens
------------------------------------------------------------------------------------------------------
Alterando, com PUT, os dados da primeira postagem do Usuário 1...                                   Ok
Alterando, com PATCH, os dados da primeira postagem do Usuário 1...                                 Ok
Tentando alterar o post do Usuário 2 com as credenciais do Usuário 1...                             Ok

Rotina de Inserção de Imagens
------------------------------------------------------------------------------------------------------
Inserindo imagens na postagem...                                                                    Ok
Tendando inserir imagens na postagem com um usuário que não é o dono da postagem...                 Ok
Tendando inserir imagens com um usuário não autenticado...                                          Ok

Rotina de Leitura de Imagens
------------------------------------------------------------------------------------------------------
Recuperando as imagens da postagem com as credenciais do Usuário 1...                               Ok
Recuperando as imagens da postagem com as credenciais do Usuário 2...                               Ok
Tentando recuperar as imagens da postagem com um usuário não autenticado...                         Ok

Rotina de Criação de Comentários
------------------------------------------------------------------------------------------------------
Inserindo comentário na Postagem 1 do Usuário 1 com as credenciais do Usuário 1...                  Ok
Inserindo comentário na Postagem 1 do Usuário 1 com as credenciais do Usuário 2...                  Ok
Tentando comentar com um usuário não autenticado...                                                 Ok

Rotina de Leitura de Comentários
------------------------------------------------------------------------------------------------------
Recuperando todos os comentários da Postagem 1 do Usuário 1 com as credenciais do Usuário 1...      Ok
Recuperando todos os comentários da Postagem 1 do Usuário 1 com as credenciais do Usuário 2...      Ok
Recuperando o Comentário 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 1...            Ok
Recuperando o Comentário 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 2...            Ok
Tentando recuperar todos os comentários com um usuários não autenticado...                          Ok
Tentando recuperar um comentário com um usuários não autenticado...                                 Ok

Rotina de Edição de Comentários
------------------------------------------------------------------------------------------------------
Tentando alterar o comentário com PATCH com as credenciais do Usuário 2...                          Ok
Tentando alterar o comentário com PUT com as credenciais do Usuário 2...                            Ok
Tentando alterar o comentário com PUT com um usuário não autenticado...                             Ok
Alterando o comentário com PATCH com as credenciais do Usuário 1...                                 Ok
Alterando o comentário com PUT com as credenciais do Usuário 1...                                   Ok

Rotina de Autenticação com Administrador
------------------------------------------------------------------------------------------------------
Realizando login como administrador...                                                              Ok

Rotina de Acesso aos Dados de Todos os Usuários
------------------------------------------------------------------------------------------------------
Tentando pegar os dados de todos os usuários com um usuário comum...                                Ok
Tentando pegar os dados de todos os usuários com um usuário não autenticado...                      Ok
Recuperando os dados de todos os usuários como administrador...                                     Ok

Rotina de Acesso ao Relatório de Utilização do Serviço
------------------------------------------------------------------------------------------------------
Tentando acessar dados estratégicos com um usuário comum...                                         Ok
Tentando acessar dados estratégicos com um usuário não autenticado...                               Ok
Recuperando informações estratégicas como administrador...                                          Ok

Rotina de Exclusão de Comentários
------------------------------------------------------------------------------------------------------
Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 utilizando as credenciais do Usuário 2...Ok
Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 com um usuário não autenticado...        Ok
Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 utilizando as credenciais do Usuário 1...Ok
Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 utilizando as credenciais do Usuário 2...Ok

Rotina de Exclusão de Imagens
------------------------------------------------------------------------------------------------------
Tentando deletar a Imagem 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 2...           Ok
Tentando deletar a Imagem 1 da Postagem 1 do Usuário 1 com um usuário não autenticado...            Ok
Deletando a Imagem 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 1...                  Ok

Rotina de Exclusão de Postagem
------------------------------------------------------------------------------------------------------
Deletando as postagens do Usuário 1 com as credenciais do Usuário 1...                              Ok
Tentando deletar o Post 1 do Usuário 2 com as credenciais do Usuário 1...                           Ok
O usuário não deve ser capaz de deletar postagens que não existem...                                Ok

Rotina de Exclusão de Usuário
------------------------------------------------------------------------------------------------------
Deletando os usuários criados...                                                                    Ok
------------------------------------------------------------------------------------------------------
Este teste demorou: 00:02:20
```

## Considerações Finais

&nbsp;&nbsp;&nbsp;&nbsp; Esse foi um projeto muito divertido de desenvolver. Se houvesse um pouquinho
mais de tempo, daria para implementar muita coisa legal. Apesar do prazo de entrega ser na terça, só
tive sábado e domingo para desenvolver todo o projeto.

<p align="right"><a href="https://www.linkedin.com/in/htgnilak/">Wallace R. Faria</a></p>
