import requests
import unittest

tc = unittest.TestCase()

def testCreateAndLogin(usersList):
    routeUser = "http://localhost:5000/users/"
    routeAuth = "http://localhost:5000/auth/"
    # Definindo usuários a serem criados
    print("Criando os Usuários e testando a realização de Login...".ljust(100), end="")

    for user in usersList:
        response = requests.post(routeUser, json=user)
        # É esperado o código 201 caso o usuário tenha sido criado corretamente.
        tc.assertEqual(response.status_code, 201)
        user["id"] = response.json()["data"]["id"]
        response = requests.post(routeAuth, auth=(user["email"], user["password"]))
        # É esperado o código 200 ao realizar login caso o usuário tenha sido criado corretamente com as credenciais
        # da usersList.
        tc.assertEqual(response.status_code, 200)
        user["token"] = response.json()["token"]
    # Não deve ser possível criar um usuário com o mesmo e-mail
    print("Ok")
    print("Tentando criar um usuário com um email que já existe...".ljust(100), end="")
    tc.assertEqual(requests.post(routeUser, json=usersList[0]).status_code, 409)
    print("Ok")

    # Não deve ser possível ter acesso ao sistema sem estar logado.
    print("Tentando acessar uma conta inexistente...".ljust(100), end="")
    tc.assertEqual(requests.post(routeAuth, auth=("teste@teste.com", "1234")).status_code, 401)
    print("Ok")

    # Não deve ser possível ter acesso ao sistema com a senha incorreta.
    print("Tentando acessar uma conta com a senha incorreta...".ljust(100), end="")
    tc.assertEqual(requests.post(routeAuth, auth=(usersList[0]["email"], "1234")).status_code, 401)
    print("Ok")
    return usersList


def testGetUsers(users):
    route = "http://localhost:5000/users/"
    headers = {"Authorization": users[0]["token"]}

    # O usuário deve ser capaz de recuperar os próprios dados
    print("Recuperando os dados do primeiro usuário com suas credenciais...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{users[0]['id']}", headers=headers).status_code, 200)
    print("Ok")

    # O usuário não deve ser capaz de recuperar os dados de outros usuários
    print("Tentando recuperar dados do segundo usuário com as credenciais do primeiro...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{users[1]['id']}", headers=headers).status_code, 401)
    print("Ok")

    # Usuários não autenticados não devem poder recuperar os dados de nenhum usuário!
    print("Tentando recuperar dados de usuários com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(f"{route}{users[0]['id']}").status_code, 401)
    tc.assertEqual(requests.get(f"{route}{users[1]['id']}").status_code, 401)
    print("Ok")


def testUpdateUsers(users):
    route = "http://localhost:5000/users/"
    headers = {"Authorization": users[0]["token"]}
    oldEmail = users[0]["email"]

    # O usuário deve ser capaz de alterar os próprios dados
    print("Alterando, com PUT, os dados do primeiro usuário com suas credenciais...".ljust(100), end="")
    users[0]["name"] = "Wallace Rocha"
    users[0]["email"] = "wallacerf@yahoo.com.br"
    users[0]["password"] = "issoEhUmaSenha"
    newData = {
        "name": users[0]["name"],
        "email": users[0]["email"],
        "password": users[0]["password"]
    }
    tc.assertEqual(requests.put(f"{route}{users[0]['id']}", json=newData, headers=headers).status_code, 200)
    print("Ok")

    # O usuário deve ser capaz de alterar os próprios dados individualmente
    print("Alterando, com PATCH, os dados do primeiro usuário com suas credenciais...".ljust(100), end="")
    newEmail = {"email": oldEmail}
    tc.assertEqual(requests.patch(f"{route}{users[0]['id']}", json=newEmail, headers=headers).status_code, 200)
    print("Ok")

    # O usuário não deve ser capaz de alterar informações críticas
    print("Tentando alterar, com PATCH, o escopo da conta do usuário com suas credenciais...".ljust(100), end="")
    tc.assertEqual(requests.patch(f"{route}{users[0]['id']}", json={"scope": "admin"}, headers=headers).status_code, 403)
    print("Ok")

    # O usuário não deve ser capaz de alterar os dados de outros usuários
    print("Tentando alterar dados do segundo usuário com as credenciais do primeiro...".ljust(100), end="")
    tc.assertEqual(requests.patch(f"{route}{users[1]['id']}", json={"password": "123"}, headers=headers).status_code, 401)
    print("Ok")


def testUserCreateReadUpdate(users):
    # Rotinas de Criação, Leitura e Edição de Usuários.
    print("", "Rotina de Criação de Usuário e Login", "-" * 102, sep="\n")
    testCreateAndLogin(users)
    print("", "Rotina de Leitura de Usuários", "-" * 102, sep="\n")
    testGetUsers(users)
    print("", "Rotina de Edição de Dados de Usuários", "-" * 102, sep="\n")
    testUpdateUsers(users)

