import requests
import unittest
tc = unittest.TestCase()


def adminAuth(admin):
    print("Realizando login como administrador...".ljust(100), end="")
    routeAuth = "http://localhost:5000/auth/"
    response = requests.post(routeAuth, auth=(admin["email"], admin["password"]))
    tc.assertEqual(response.status_code, 200)
    admin["token"] = response.json()["token"]
    print("Ok")


def getAllUsers(user, admin):
    route = "http://localhost:5000/users/"
    headersUser, headersAdmin = {"Authorization": user["token"]}, {"Authorization": admin["token"]}

    # Usuários comuns ou não autenticados não devem poder acessar os dados de todos os usuários
    print("Tentando pegar os dados de todos os usuários com um usuário comum...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersUser).status_code, 401)
    print("Ok")

    print("Tentando pegar os dados de todos os usuários com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(route).status_code, 401)
    print("Ok")

    # Administradores devem poder acessar os dados de todos os usuários
    print("Recuperando os dados de todos os usuários como administrador...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersAdmin).status_code, 200)
    print("Ok")


def getSummary(user, admin):
    route = "http://localhost:5000/summary/"
    headersUser, headersAdmin = {"Authorization": user["token"]}, {"Authorization": admin["token"]}

    # Usuários comuns ou não autenticados não devem poder acessar os dados estratégicos da plataforma
    print("Tentando acessar dados estratégicos com um usuário comum...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersUser).status_code, 401)
    print("Ok")

    print("Tentando acessar dados estratégicos com um usuário não autenticado...".ljust(100), end="")
    tc.assertEqual(requests.get(route).status_code, 401)
    print("Ok")

    # Administradores devem poder acessar os dados de todos os usuários
    print("Recuperando informações estratégicas como administrador...".ljust(100), end="")
    tc.assertEqual(requests.get(route, headers=headersAdmin).status_code, 200)
    print("Ok")


def testAdminScope(user, admin):
    # Primeiramente, será realizado o login com as credenciais de administrador.
    print("", "Rotina de Autenticação com Administrador", "-" * 102, sep="\n")
    adminAuth(admin)
    print("", "Rotina de Acesso aos Dados de Todos os Usuários", "-" * 102, sep="\n")
    getAllUsers(user, admin)
    print("", "Rotina de Acesso ao Relatório de Utilização do Serviço", "-" * 102, sep="\n")
    getSummary(user, admin)
