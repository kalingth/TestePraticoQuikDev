from APP import app, db
from ..Controller import authenticator
from ..Views import admin


@app.route('/summary/', methods=['GET'])
@authenticator.requireToken
def getSummary(authenticatedUser: db.Model):
    return admin.summary(authenticatedUser)


@app.route('/users/', methods=['GET'])
@authenticator.requireToken
def getAllUsers(authenticatedUser: db.Model) -> tuple:
    return admin.getAllUsers(authenticatedUser)