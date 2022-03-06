from APP import app, db
from ..Controller import authenticator
from ..Views import posts
from flask import request


@app.route('/posts/', methods=['POST'])
@authenticator.requireToken
def createNewPost(authenticatedUser: db.Model) -> tuple:
    return posts.makeAPost(authenticatedUser)


@app.route('/posts/<int:identifier>/', methods=['PATCH', 'GET', 'DELETE', 'PUT'])
@authenticator.requireToken
def readUpdateDeletePosts(identifier: int, authenticatedUser: db.Model) -> tuple:
    functions = {
        'GET': posts.getPost,
        'PUT': posts.updatePostWithPut,
        'PATCH': posts.updatePostWithPatch,
        'DELETE': posts.deletePost
    }
    return functions[request.method](identifier, authenticatedUser=authenticatedUser)


@app.route('/posts/<int:postId>/images/', methods=['POST', 'GET'])
@authenticator.requireToken
def uploadAnImage(postId, authenticatedUser: db.Model) -> tuple:
    functions = {
        'GET': posts.readImage,
        'POST': posts.imageInput
    }
    return functions[request.method](postId, authenticatedUser)


@app.route('/posts/<int:postId>/images/<int:imageId>/', methods=['DELETE'])
@authenticator.requireToken
def readDeleteImage(postId: int, imageId: int, authenticatedUser: db.Model) -> tuple:
    return posts.deleteImage(postId, imageId, authenticatedUser)
