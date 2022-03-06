from APP import db
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from ..Models.comments import Comment, comment_schema, comments_schema
from ..Models.posts import Post
from ..Models.users import Users
from ..Controller.notifier import notifyPostOwner
import MISC.CONSTANTS as CONSTS


def makeAComment(postId: int, authenticatedUser: db.Model) -> tuple:
    try:
        userId = authenticatedUser.id
        postId = postId
        description = request.json["description"]
        comment = Comment(userId, postId, description)
        db.session.add(comment)
        db.session.commit()
        result = comment_schema.dump(comment)

        post = Post.query.get(postId)
        postOwner = Users.query.get(post.user_id)
        if postOwner.email != authenticatedUser.email:
            notifyPostOwner(postOwner, authenticatedUser, post, comment)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 201
    except KeyError:
        return jsonify({"success": False, "message": CONSTS.Messages.ATTRIBUTE_NOT_FOUND, "data": {}}), 400
    except IntegrityError:
        return jsonify({"success": False, "message": "That request seems wrong!", "data": {}}), 400
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def getComment(postId: int, commentId: int, authenticatedUser: db.Model) -> tuple:
    if not authenticatedUser:
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        if not (comment := Comment.query.get(commentId)):
            return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
        result = comment_schema.dump(comment)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def getAllComments(postId: int, authenticatedUser: db.Model) -> tuple:
    if not authenticatedUser:
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        if not (comments := Comment.query.filter(Comment.post_id == postId)):
            return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
        result = comments_schema.dump(comments)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": {"comments": result}}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def updateComment(postId: int, commentId: int, authenticatedUser: db.Model) -> tuple:
    data = request.json
    if not (comment := Comment.query.get(commentId)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if not authenticatedUser or (authenticatedUser.id != comment.user_id and authenticatedUser.scope != "admin"):
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401

    commonScope = Comment.myCommentEditableAttributesForCommonScope()
    if not all(key in commonScope for key in data.keys()) and authenticatedUser.scope == "common":
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_REACHABLE, "data": {}}), 403

    adminScope = Comment.myCommentEditableAttributesForAdminScope()
    if not all(key in adminScope for key in data.keys()) and authenticatedUser.scope == "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404

    try:
        for key, value in data.items():
            setattr(comment, key, value)
        db.session.commit()
        result = comment_schema.dump(comment)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def deleteComment(postId: int, commentId: int, authenticatedUser: db.Model) -> tuple:
    if not (comment := Comment.query.get(commentId)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    post = Post.query.get(postId)

    if authenticatedUser.id not in (comment.user_id, post.user_id) and authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401

    try:
        db.session.delete(comment)
        db.session.commit()
        result = comment_schema.dump(comment)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500
