from APP import db
from mailjet_rest import Client
import MISC.CONSTANTS
import copy


def processTemplate(template: str, **kwargs: dict) -> str:
    processedTemplate = copy.copy(template)
    for key, value in kwargs.items():
        processedTemplate = processedTemplate.replace(key, value)
    return processedTemplate


def notifyPostOwner(postOwner: db.Model, commentOwner: db.Model, post: db.Model, comment: db.Model) -> None:
    mailjet = Client(auth=(MISC.CONSTANTS.MAILJET_API_KEY, MISC.CONSTANTS.MAILJET_API_SECRET), version='v3.1')
    toReplace = {
      "{{nameOfUserPost}}": postOwner.name,
      "{{titlePost}}": post.title,
      "{{nameOfUserComment}}": commentOwner.name,
      "{{contentOfComment}}": comment.description
    }
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "no-reply@kalingth.com.br",
                    "Name": "Kalingth's Corp."
                },
                "To": [
                    {
                        "Email": postOwner.email,
                        "Name": postOwner.name
                    }
                ],
                "Subject": "A new comment has been done into your post!",
                "TextPart": "Comment Notify for the App User.",
                "HTMLPart": processTemplate(MISC.CONSTANTS.MAIL_TEMPLATE, **toReplace),
                "CustomID": "NotifyCommentQuikDevTest"
            }
        ]
    }
    mailjet.send.create(data=data)
