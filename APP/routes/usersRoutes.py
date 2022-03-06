from APP import app, db
from ..Controller import authenticator
from ..Views import users
from flask import request


@app.route('/users/', methods=['POST'])
def createUser() -> tuple:
    return users.createUser()


@app.route('/users/<int:identifier>/', methods=['PATCH', 'PUT', 'GET', 'DELETE'])
@authenticator.requireToken
def readUpdateDeleteUser(identifier: int, authenticatedUser: db.Model) -> tuple:
    functions = {
        'GET': users.getUser,
        'PATCH': users.patchUpdateUser,
        'PUT': users.putUpdateUsers,
        'DELETE': users.deleteUser
    }
    return functions[request.method](identifier, authenticatedUser=authenticatedUser)
