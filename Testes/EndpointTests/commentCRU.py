import requests
import unittest
tc = unittest.TestCase()


def testCreateComment(users):
    user1, user2 = users[0], users[1]
    user1["comments"], user2["comments"] = [], []
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    route = f"http://localhost:5000/posts/{post1}/comments/"

    # O usuário deverá poder comentar em suas próprias postagens.
    # Os comentários do próprio usuário não dispararão um email de notificação.
    print("Inserindo comentário na Postagem 1 do Usuário 1 com as credenciais do Usuário 1...".ljust(100), end="")
    payload = {"description": "This is my first comment!"}
    response = requests.post(route, json=payload, headers=headersUser1)
    user1["comments"].append(response.json()["data"]["id"])
    tc.assertEqual(response.status_code, 201)
    print("Ok")

    # O usuário deverá poder comentar nas postagens dos outros usuários.
    # Esse comentário deverá disparar uma notificação!
    print("Inserindo comentário na Postagem 1 do Usuário 1 com as credenciais do Usuário 2...".ljust(100), end="")
    payload = {"description": "This is my first comment too!"}
    response = requests.post(route, json=payload, headers=headersUser2)
    user2["comments"].append(response.json()["data"]["id"])
    tc.assertEqual(response.status_code, 201)
    print("Ok")

    # Usuários não autenticados não poderem comentar as postagens.
    print("Tentando comentar com um usuário não autenticado...".ljust(100), end="")
    payload = {"description": "This is my first comment too!"}
    response = requests.post(route, json=payload)
    tc.assertEqual(response.status_code, 401)
    print("Ok")


def testReadComment(users):
    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    comment1 = user1["comments"][0]
    route = f"http://localhost:5000/posts/{post1}/comments/"

    # Os usuários devem ser capazes de recuperar uma lista de todos os comentários de um post.
    print("Recuperando todos os comentários da Postagem 1 do Usuário 1 com as credenciais do Usuário 1...".ljust(100), end="")
    response = requests.get(route, headers=headersUser1)
    tc.assertEqual(response.status_code, 200)
    tc.assertEqual(type(response.json()["data"]["comments"]), list)
    print("Ok")

    print("Recuperando todos os comentários da Postagem 1 do Usuário 1 com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersUser2).status_code, 200)
    print("Ok")

    # Os usuários devem ser capazes de recuperar cada comentário individualmente.
    print("Recuperando o Comentário 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 1...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{comment1}", headers=headersUser1).status_code, 200)
    print("Ok")

    print("Recuperando o Comentário 1 da Postagem 1 do Usuário 1 com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{comment1}", headers=headersUser2).status_code, 200)
    print("Ok")

    # Usuários não autenticados não devem conseguir ler nenhum comentário.
    print("Tentando recuperar todos os comentários com um usuários não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(route).status_code, 401)
    print("Ok")

    print("Tentando recuperar um comentário com um usuários não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{comment1}").status_code, 401)
    print("Ok")


def testUpdateComment(users):
    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    comment1 = user1["comments"][0]
    route = f"http://localhost:5000/posts/{post1}/comments/{comment1}"

    # Outros usuários, senão o dono do comentário, não devem poder editar o comentário de forma alguma.
    payload = {"description": "I'll change this!!"}
    print("Tentando alterar o comentário com PATCH com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.patch(f"{route}", json=payload, headers=headersUser2).status_code, 401)
    print("Ok")

    print("Tentando alterar o comentário com PUT com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.put(f"{route}", json=payload, headers=headersUser2).status_code, 401)
    print("Ok")

    print("Tentando alterar o comentário com PUT com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.put(f"{route}", json=payload).status_code, 401)
    print("Ok")

    # Como destacado anteriormente, o dono do comentário deverá poder alterar o comentário.
    payload = {"description": "No, only I can change this!!"}
    print("Alterando o comentário com PATCH com as credenciais do Usuário 1...".ljust(100), end="")
    tc.assertEqual(requests.patch(f"{route}", json=payload, headers=headersUser1).status_code, 200)
    print("Ok")

    payload = {"description": "One more time, I'll change this!! Deal with it!!"}
    print("Alterando o comentário com PUT com as credenciais do Usuário 1...".ljust(100), end="")
    tc.assertEqual(requests.put(f"{route}", json=payload, headers=headersUser1).status_code, 200)
    print("Ok")


def testCommentCreateReadUpdate(users):
    # Rotina de Criação, Leitura e Exclusão de Comentários.
    print("", "Rotina de Criação de Comentários", "-" * 102, sep="\n")
    testCreateComment(users)
    print("", "Rotina de Leitura de Comentários", "-" * 102, sep="\n")
    testReadComment(users)
    print("", "Rotina de Edição de Comentários", "-" * 102, sep="\n")
    testUpdateComment(users)

