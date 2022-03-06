import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from datetime import datetime, timedelta
from hashlib import sha512
from flask import request, jsonify
from functools import wraps

from .. import app
from ..Views.users import userByEmailOrId
from ..Models.users import user_schema, Users

import MISC.CONSTANTS as CONSTS
from collections.abc import Callable

def auth() -> tuple:
    authorization = request.authorization
    if not all([authorization, authorization.username, authorization.password]):
        return jsonify({"success": False, "message": "Login required!", "data": {}}), 401
    if not (user := userByEmailOrId(authorization.username, )):
        return jsonify({"success": False, "message": "User or password are wrong!", "data": {}}), 401
    try:
        if user.password == str(sha512(authorization.password.encode()).hexdigest()):
            token = jwt.encode({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "exp": datetime.now() + timedelta(hours=6)
            }, app.config["SECRET_KEY"])
            result = user_schema.dump(user)
            return jsonify({"success": True, "message": f"Welcome, {user.name}!", "token": token, "data": result}), 200
        else:
            return jsonify({"success": False, "message": "User or password are wrong!", "token": None, "data": {}}), 401
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def requireToken(function: Callable) -> Callable:
    @wraps(function)
    def decoratedPreProcess(*args: tuple, **kwargs: dict) -> tuple:
        try:
            if not (token := request.headers["Authorization"].split()[-1]):
                return jsonify({"success": False, "message": "Authorization token not found!", "data": {}}), 401
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])
            currentUser = userByEmailOrId(data["email"], data["id"])
        except KeyError:
            return jsonify({"success": False, "message": "You need to inform the Authorization Header.", "data": {}}), 401
        except DecodeError:
            return jsonify({"success": False, "message": "This isn't a valid token.", "data": {}}), 401
        except ExpiredSignatureError:
            return jsonify({"success": False, "message": "This token was expired.", "data": {}}), 401
        except Exception as e:
            print(e)
            return jsonify({"success": False, "message":  CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500
        return function(*args, authenticatedUser=currentUser, **kwargs)
    return decoratedPreProcess

