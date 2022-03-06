import base64
import requests
import unittest
from os import path
tc = unittest.TestCase()


def testCreatePosts(users):
    route = "http://localhost:5000/posts/"
    postsUser1 = [
        {"title": "Hello World", "description": "My First Post"},
        {"title": "My Second Post", "description": "Wow!! This platform is awesome!"},
        {"title": "Hi Guys", "description": "Hi guys, please, comment at this post"}
    ]

    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    user1["posts"], user2["posts"] = [], []

    # O usuário deve poder criar postagens!
    print("Criando postagens como o Usuário 1...".ljust(100), end="")
    for postUser1 in postsUser1:
        response = requests.post(route, json=postUser1, headers={"Authorization": user1["token"]})
        # É esperado o código 201 caso o post tenha sido criado corretamente.
        tc.assertEqual(response.status_code, 201)
        user1["posts"].append(response.json()["data"]["id"])
    print("Ok")

    # O usuário não deve poder criar postagens caso estejam faltando dados na requisição!
    print("Tentando criar postagens como o Usuário 1 com uma requisição incompleta...".ljust(100), end="")
    payload = {"title": "Quero criar só o title!!"}
    tc.assertEqual(requests.post(route, json=payload, headers=headersUser1).status_code, 400)
    print("Ok")

    # Outros usuários também devem poder criar seus próprios posts.
    print("Tentando criar postagens como o Usuário 2...".ljust(100), end="")
    payload = {"title": "Olha eu aqui!!", "description": "Br também usa a plataforma!!"}
    response = requests.post(route, json=payload, headers=headersUser2)
    tc.assertEqual(response.status_code, 201)
    tc.assertEqual(response.json()["data"]["user_id"], user2["id"])
    user2["posts"].append(response.json()["data"]["id"])
    print("Ok")


def testGetPosts(users):
    route = "http://localhost:5000/posts/"
    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    postUser1, postUser2 = user1["posts"][0], user2["posts"][0]

    # O Usuário 1 deverá ser capaz de recuperar suas próprias postagens
    print("Recuperando a primeira postagem do Usuário 1 com suas credenciais...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{postUser1}", headers=headersUser1).status_code, 200)
    print("Ok")

    # O Usuário 2 deverá ser capaz de recuperar as postagens do Usuário 1
    print("Recuperando a primeira postagem do Usuário 1 com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{postUser1}", headers=headersUser2).status_code, 200)
    print("Ok")

    # Usuários não autenticados não devem poder recuperar os dados de nenhuma postagem!
    print("Tentando recuperar postagens com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{postUser1}").status_code, 401)
    tc.assertEqual(requests.get(f"{route}{postUser2}").status_code, 401)
    print("Ok")


def testUpdatePosts(users):
    route = "http://localhost:5000/posts/"
    user1 = users[0]
    headersUser1 = {"Authorization": user1["token"]}
    post1 = user1["posts"][0]
    post1User2 = users[1]["posts"][0]

    # O usuário deve poder editar seus posts com PUT
    print("Alterando, com PUT, os dados da primeira postagem do Usuário 1...".ljust(100), end="")
    payload = {"title": "World, Hello!", "description": "Now, I made a lot of posts!"}
    tc.assertEqual(requests.put(f"{route}{post1}", json=payload, headers=headersUser1).status_code, 200)
    print("Ok")

    # O usuário deve poder editar seus posts com PATCH
    print("Alterando, com PATCH, os dados da primeira postagem do Usuário 1...".ljust(100), end="")
    payload = {"title": "Hello my loved World!"}
    tc.assertEqual(requests.patch(f"{route}{post1}", json=payload, headers=headersUser1).status_code, 200)
    print("Ok")

    # O usuário não deve poder editar os posts dos outros usuários.
    print("Tentando alterar o post do Usuário 2 com as credenciais do Usuário 1...".ljust(100), end="")
    payload = {"title": "Hello my loved World!"}
    tc.assertEqual(requests.patch(f"{route}{post1User2}", json=payload, headers=headersUser1).status_code, 401)
    print("Ok")


def testUploadImage(users):
    user1, user2 = users[0], users[1]
    user1["uploads"], user2["uploads"] = [], []
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    route = f"http://localhost:5000/posts/{post1}/images"

    dir_path = path.dirname(path.realpath(__file__))
    image = path.join(dir_path, "QuikDevLogo.png")
    with open(image, "rb") as file:
        img_b64 = base64.b64encode(file.read()).decode("utf-8")

    # O dono da postagem pode adicionar imagens a ela.
    print("Inserindo imagens na postagem...".ljust(100), end="")
    payload = {"b64_image": img_b64}
    response = requests.post(route, json=payload, headers=headersUser1)
    user1["uploads"].append(response.json()["data"]["id"])
    tc.assertEqual(response.status_code, 201)
    print("Ok")

    # Outros usuários não devem poder inserir imagens na postagem.
    print("Tendando inserir imagens na postagem com um usuário que não é o dono da postagem...".ljust(100), end="")
    payload = {"b64_image": img_b64}
    response = requests.post(route, json=payload, headers=headersUser2)
    tc.assertEqual(response.status_code, 401)
    print("Ok")

    # Usuários não autenticados não podem inserir imagens nas postagens.
    print("Tendando inserir imagens com um usuário não autenticado...".ljust(100), end="")
    payload = {"b64_image": img_b64}
    response = requests.post(route, json=payload)
    tc.assertEqual(response.status_code, 401)
    print("Ok")


def testGetImage(users):
    user1, user2 = users[0], users[1]
    headersUser1, headersUser2 = {"Authorization": user1["token"]}, {"Authorization": user2["token"]}
    post1 = user1["posts"][0]
    route = f"http://localhost:5000/posts/{post1}/images"

    # Os usuários devem recuperar todas as imagens relativas a uma postagem.
    print("Recuperando as imagens da postagem com as credenciais do Usuário 1...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersUser1).status_code, 200)
    print("Ok")

    print("Recuperando as imagens da postagem com as credenciais do Usuário 2...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersUser2).status_code, 200)
    print("Ok")

    # Um usuário não autenticado não pode recuperar as imagens.
    print("Tentando recuperar as imagens da postagem com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(route).status_code, 401)
    print("Ok")


def testPostCreateReadUpdateUpload(users):
    # Rotinas de Criação, Leitura e Edição de Posts.
    print("", "Rotina de Criação de Postagens", "-" * 102, sep="\n")
    testCreatePosts(users)
    print("", "Rotina de Leitura de Postagens", "-" * 102, sep="\n")
    testGetPosts(users)
    print("", "Rotina de Edição de Postagens", "-" * 102, sep="\n")
    testUpdatePosts(users)

    # > Subrotina de inserção de imagens
    print("", "Rotina de Inserção de Imagens", "-" * 102, sep="\n")
    testUploadImage(users)
    print("", "Rotina de Leitura de Imagens", "-" * 102, sep="\n")
    testGetImage(users)
