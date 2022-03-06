import requests
import unittest

tc = unittest.TestCase()


def testDeleteComments(users):
    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    comment1 = user1["comments"][0]
    comment2 = user2["comments"][0]
    route = f"http://localhost:5000/posts/{post1}/comments/{comment1}"

    # Outro usuário, que não seja o dono do comentário, o dono do post ou o administrador,
    # não deve poder deletar o comentário
    print("Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 utilizando as credenciais do Usuário 2..."
          .ljust(100), end="")
    tc.assertEqual(requests.delete(route, headers=headersUser2).status_code, 401)
    print("Ok")

    print("Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 com um usuário não autenticado..."
          .ljust(100), end="")
    tc.assertEqual(requests.delete(route).status_code, 401)
    print("Ok")

    # O dono do comentário deve poder deletar o seu próprio comentário.
    print("Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 utilizando as credenciais do Usuário 1..."
          .ljust(100), end="")
    tc.assertEqual(requests.delete(route, headers=headersUser1).status_code, 200)
    print("Ok")

    # O dono da postagem deve poder deletar o comentário de outros usuários em sua própria postagem.
    route = f"http://localhost:5000/posts/{post1}/comments/{comment2}"
    print("Tentando deletar o Comentário 1 da Postagem 1 do Usuário 1 utilizando as credenciais do Usuário 2..."
          .ljust(100), end="")
    tc.assertEqual(requests.delete(route, headers=headersUser1).status_code, 200)
    print("Ok")


def testDeleteImage(users):
    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    image1 = user1["uploads"][0]
    route = f"http://localhost:5000/posts/{post1}/images/{image1}"

    # Outros usuários, se não o próprio dono da postagem, não podem deletar as imagens das postagens
    print("Tentando deletar a Imagem 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.delete(route, headers=headersUser2).status_code, 401)
    print("Ok")

    # Um usuário não autenticado não pode deletar as imagens.
    print("Tentando deletar a Imagem 1 da Postagem 1 do Usuário 1 com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.delete(route).status_code, 401)
    print("Ok")

    print("Deletando a Imagem 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 1...".ljust(100), end="")
    tc.assertEqual(requests.delete(route, headers=headersUser1).status_code, 200)
    print("Ok")


def testDeletePosts(users):
    route = "http://localhost:5000/posts/"

    # O usuário deve poder deletar suas postagens!
    print("Deletando as postagens do Usuário 1 com as credenciais do Usuário 1...".ljust(100), end="")
    user1 = users[0]
    headersUser1 = {"Authorization": user1["token"]}
    while user1["posts"]:
        response = requests.delete(f"{route}{(lastId := user1['posts'].pop())}", headers=headersUser1)
        tc.assertEqual(response.status_code, 200)
    print("Ok")

    # O usuário não deve poder deletar as postagens de outros usuários!
    print("Tentando deletar o Post 1 do Usuário 2 com as credenciais do Usuário 1...".ljust(100), end="")
    response = requests.delete(f"{route}{users[1]['posts'][0]}", headers=headersUser1)
    tc.assertEqual(response.status_code, 401)
    print("Ok")

    # Não é possível deletar dados inexistentes.
    print("O usuário não deve ser capaz de deletar postagens que não existem...".ljust(100), end="")
    response = requests.delete(f"{route}{lastId}", headers=headersUser1)
    tc.assertEqual(response.status_code, 404)
    print("Ok")


def testUsersDelete(users):
    route = "http://localhost:5000/users/"
    print("Deletando os usuários criados...".ljust(100), end="")
    for user in users:
        response = requests.delete(f"{route}{user['id']}", headers={"Authorization": user["token"]})
        # O usuário deverá ser deletado!
        tc.assertEqual(response.status_code, 200)
    print("Ok")
    users = []


def completeDeleteRoutine(users):
    # Rotinas de Exclusão
    print("", "Rotina de Exclusão de Comentários", "-" * 102, sep="\n")
    testDeleteComments(users)
    print("", "Rotina de Exclusão de Imagens", "-" * 102, sep="\n")
    testDeleteImage(users)
    print("", "Rotina de Exclusão de Postagem", "-" * 102, sep="\n")
    testDeletePosts(users)
    print("", "Rotina de Exclusão de Usuário", "-" * 102, sep="\n")
    testUsersDelete(users)
