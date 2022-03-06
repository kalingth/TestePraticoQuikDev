from APP import db
from flask import jsonify
from sqlalchemy import func
from ..Models.users import Users, users_schema
from ..Models.posts import Post
from ..Models.comments import Comment
import MISC.CONSTANTS as CONSTS


def getAllUsers(authenticatedUser: db.Model) -> tuple:
    if not authenticatedUser or authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        users = Users.query.all()
        result = users_schema.dump(users)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": {"list": result}}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def summary(authenticatedUser: db.Model):
    if not authenticatedUser or authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        data = db.session.query(Post.title, func.count(Comment.id)).join(Comment, Post.id == Comment.post_id).all()
        toDict = [ {"title": title, "n_comments": n_comments} for title, n_comments in data]
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": {"summary": toDict}}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500
