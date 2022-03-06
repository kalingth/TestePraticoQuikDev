from APP import db, ma
from .users import Users
from .posts import Post
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey(Users.id), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey(Post.id), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user = relationship(Users)
    post = relationship(Post)

    @staticmethod
    def myCommentEditableAttributesForAdminScope():
        return 'user_id', 'post_id'

    @staticmethod
    def myCommentEditableAttributesForCommonScope():
        return 'description',

    def __repr__(self):
        return f"<Comment {self.id} into Post {self.post_id} by User {self.user_id}>"

    def __init__(self, user_id, post_Id, description):
        self.user_id = user_id
        self.post_id = post_Id
        self.description = description


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'post_id', 'description')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
