from APP import app, db
from ..Controller import authenticator
from ..Views import comments
from flask import request


@app.route('/posts/<int:postId>/comments/', methods=['POST', 'GET'])
@authenticator.requireToken
def createGetNewComment(postId: int, authenticatedUser: db.Model) -> tuple:
    functions = {
        'GET': comments.getAllComments,
        'POST': comments.makeAComment
    }
    return functions[request.method](postId, authenticatedUser)


@app.route('/posts/<int:postId>/comments/<int:commentId>', methods=['PATCH', 'GET', 'PUT', 'DELETE'])
@authenticator.requireToken
def readUpdateDeleteComments(postId: int, commentId: int, authenticatedUser: db.Model) -> tuple:
    functions = {
        'GET': comments.getComment,
        'PATCH': comments.updateComment,
        'PUT': comments.updateComment,
        'DELETE': comments.deleteComment
    }
    return functions[request.method](postId, commentId, authenticatedUser=authenticatedUser)
