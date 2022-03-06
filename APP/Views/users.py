from APP import db
from hashlib import sha512
from flask import request, jsonify
from ..Models.users import Users, user_schema
from sqlalchemy.exc import IntegrityError, NoResultFound
import MISC.CONSTANTS as CONSTS


def createUser() -> tuple:
    try:
        email = request.json["email"]
        password = request.json["password"]
        name = request.json["name"]
        passwordHash = str(sha512(password.encode()).hexdigest())
        user = Users(email, passwordHash, name)
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 201
    except KeyError:
        return jsonify({"success": False, "message": CONSTS.Messages.ATTRIBUTE_NOT_FOUND, "data": {}}), 400
    except IntegrityError:
        return jsonify({"success": False, "message": "User already created!", "data": {}}), 409
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def getUser(identifier: id, authenticatedUser: db.Model) -> tuple:
    try:
        if not (user := Users.query.get(identifier)):
            return jsonify({"success": False, "message": "That user doesn't exist!", "data": {}}), 404
        if not authenticatedUser or (user.email != authenticatedUser.email and authenticatedUser.scope != "admin"):
            return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
        result = user_schema.dump(user)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def putUpdateUsers(identifier: int, authenticatedUser: db.Model) -> tuple:
    if not (user := Users.query.get(identifier)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if not authenticatedUser or (user.email != authenticatedUser.email and authenticatedUser.scope != "admin"):
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        password = request.json["password"]
        user.email = request.json["email"]
        user.name = request.json["name"]
        user.password = str(sha512(password.encode()).hexdigest())
        # user.scope = user.scope if authenticatedUser.scope != "admin" else request.json["scope"]
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except KeyError:
        return jsonify({"success": False, "message": CONSTS.Messages.ATTRIBUTE_NOT_FOUND, "data": {}}), 400
    except IntegrityError:
        return jsonify({"success": False, "message": "That e-mail is already in use!", "data": {}}), 409
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def patchUpdateUser(identifier: int, authenticatedUser: db.Model) -> tuple:
    if not (user := Users.query.get(identifier)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if not authenticatedUser or (user.email != authenticatedUser.email and authenticatedUser.scope != "admin"):
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    if "password" in (data := request.json).keys():
        data["password"] = str(sha512(data["password"].encode()).hexdigest())

    commonScope = Users.myUserEditableAttributesForCommonScope()
    if not all(key in commonScope for key in data.keys()) and authenticatedUser.scope == "common":
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_REACHABLE, "data": {}}), 403

    adminScope = Users.myUserEditableAttributesForAdminScope()
    if not all(key in adminScope for key in data.keys()) and authenticatedUser.scope == "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404

    try:
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except IntegrityError:
        return jsonify({"success": False, "message": "That e-mail is already in use!", "data": {}}), 409
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def deleteUser(identifier: int, authenticatedUser: db.Model) -> tuple:
    if not (user := Users.query.get(identifier)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if not authenticatedUser or (user.email != authenticatedUser.email and authenticatedUser.scope != "admin"):
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        db.session.delete(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def userByEmailOrId(email: str, id: int = None) -> (db.Model, None):
    try:
        user = Users.query.filter(Users.email == email).one()
    except NoResultFound:
        user = Users.query.get(id)
    except Exception as e:
        print(e)
        return None
    return user
