from APP import db, ma


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(191), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    scope = db.Column(db.String(6), nullable=False)

    @staticmethod
    def myUserEditableAttributesForCommonScope():
        return "email", "password", "name"

    @staticmethod
    def myUserEditableAttributesForAdminScope():
        return "email", "password", "name", "scope"

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"

    def __init__(self, email, password, name, scope="common"):
        self.email = email
        self.password = password
        self.name = name
        self.scope = scope


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name')


class UsersSchema4Admin(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'name', 'scope')


user_schema = UsersSchema()
users_schema = UsersSchema4Admin(many=True)
