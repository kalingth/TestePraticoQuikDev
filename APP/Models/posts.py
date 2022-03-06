from APP import db, ma
from .users import Users
from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import relationship


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey(Users.id), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user = relationship(Users)

    @staticmethod
    def myPostEditableAttributesForCommonScope():
        return "title", "description"

    @staticmethod
    def myPostEditableAttributesForAdminScope():
        return "user_id", "title", "description"

    def __repr__(self):
        return f"<Post {self.id} by {self.user_id}: {self.title}>"

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'title', 'description')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, ForeignKey(Post.id), nullable=False)
    image_blob = db.Column(types.LargeBinary, nullable=False)
    post = relationship(Post)

    def __init__(self, post_id, blob):
        self.post_id = post_id
        self.image_blob = blob


class PostImageSchemaWithBlob(ma.Schema):
    class Meta:
        fields = ('id', 'post_id', 'image_blob')


class PostImageSchemaWithoutBlob(ma.Schema):
    class Meta:
        fields = ('id', 'post_id')


pImage_schema = PostImageSchemaWithBlob(many="True")
pImageNoBlob_schema = PostImageSchemaWithoutBlob()
