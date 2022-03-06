from flask import jsonify
import MISC.CONSTANTS
import traceback
from .adminRoutes import getSummary, getAllUsers, authenticator, app
from .usersRoutes import readUpdateDeleteUser, createUser
from .postsRoutes import createNewPost, readUpdateDeletePosts, uploadAnImage, readDeleteImage
from .commentsRoutes import createGetNewComment, readUpdateDeleteComments


@app.errorhandler(404)
def notFound(e) -> tuple:
    print(traceback.format_exc())
    print(e)
    return jsonify({"success": False, "message": MISC.CONSTANTS.Messages.RESOURCE_NOT_FOUND, "data": {}}), 404


@app.errorhandler(405)
def methodNotAllowed(e) -> tuple:
    print(traceback.format_exc())
    print(e)
    return jsonify({"success": False, "message": "Method not allowed for this route!"}), 405


@app.errorhandler(500)
def internalServerError(e) -> tuple:
    print(traceback.format_exc())
    print(e)
    return jsonify({"success": False, "message": MISC.CONSTANTS.Messages.DEFAULT_SERVER_ERROR, "data": {}}), 500


@app.route('/auth/', methods=['POST'])
def authenticate() -> tuple:
    return authenticator.auth()
