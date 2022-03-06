from APP import db
import base64
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from ..Models.posts import *
import MISC.CONSTANTS as CONSTS


def makeAPost(authenticatedUser: db.Model) -> tuple:
    try:
        userId = authenticatedUser.id
        title = request.json["title"]
        description = request.json["description"]

        post = Post(userId, title, description)
        db.session.add(post)
        db.session.commit()
        result = post_schema.dump(post)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 201
    except KeyError:
        return jsonify({"success": False, "message": CONSTS.Messages.ATTRIBUTE_NOT_FOUND, "data": {}}), 400
    except IntegrityError:
        return jsonify({"success": False, "message": "That request seems wrong!", "data": {}}), 400
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def getPost(identifier: int, authenticatedUser: db.Model) -> tuple:
    try:
        if not (post := Post.query.get(identifier)):
            return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
        result = post_schema.dump(post)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def updatePostWithPatch(identifier: int, authenticatedUser: db.Model) -> tuple:
    data = request.json
    if not (post := Post.query.get(identifier)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if authenticatedUser.id != post.user_id and authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    commonScope = Post.myPostEditableAttributesForCommonScope()
    if not all(key in commonScope for key in data.keys()) and authenticatedUser.scope == "common":
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_REACHABLE, "data": {}}), 403
    adminScope = Post.myPostEditableAttributesForAdminScope()
    if not all(key in adminScope for key in data.keys()) and authenticatedUser.scope == "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    try:
        for key, value in data.items():
            setattr(post, key, value)
        db.session.commit()
        result = post_schema.dump(post)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def updatePostWithPut(identifier: int, authenticatedUser: db.Model) -> tuple:
    if not (post := Post.query.get(identifier)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if authenticatedUser.id != post.user_id and authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401

    try:
        post.title = request.json["title"]
        post.description = request.json["description"]
        db.session.commit()
        result = post_schema.dump(post)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def deletePost(identifier: int, authenticatedUser: db.Model) -> tuple:
    if not (post := Post.query.get(identifier)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if authenticatedUser.id != post.user_id and authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        db.session.delete(post)
        db.session.commit()
        result = post_schema.dump(post)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def imageInput(postId: int, authenticatedUser: db.Model) -> tuple:
    if not (post := Post.query.get(postId)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if authenticatedUser.scope != "admin" and post.user_id != authenticatedUser.id:
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        blob = base64.b64decode(request.json["b64_image"])
        postImage = PostImages(postId, blob)
        db.session.add(postImage)
        db.session.commit()
        result = pImageNoBlob_schema.dump(postImage)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 201
    except KeyError:
        return jsonify({"success": False, "message": CONSTS.Messages.ATTRIBUTE_NOT_FOUND, "data": {}}), 400
    except IntegrityError:
        return jsonify({"success": False, "message": "That request seems wrong!", "data": {}}), 400
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def processImagesBeforeSend(images: list) -> list:
    output = []
    for image in images:
        output.append({
            "id": image.id,
            "post_id": image.post_id,
            "b64_image": base64.b64encode(image.image_blob).decode("UTF-8")
        })
    return output


def readImage(postId: int, authenticatedUser: db.Model) -> tuple:
    if not Post.query.get(postId):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    try:
        images = PostImages.query.filter(PostImages.post_id == postId)
        result = processImagesBeforeSend(images)

        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": {"images": result}}), 200
    except Exception as e:
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


def deleteImage(postId: int, imageId: int, authenticatedUser: db.Model) -> tuple:
    if not (postImage := PostImages.query.get(imageId)):
        return jsonify({"success": False, "message": CONSTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404
    if Post.query.get(postId).user_id != authenticatedUser.id and authenticatedUser.scope != "admin":
        return jsonify({"success": False, "message": CONSTS.Messages.UNAUTHORIZATED, "data": {}}), 401
    try:
        db.session.delete(postImage)
        db.session.commit()
        result = pImageNoBlob_schema.dump(postImage)
        return jsonify({"success": True, "message": CONSTS.Messages.SUCCESS_MESSAGE, "data": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": CONSTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500