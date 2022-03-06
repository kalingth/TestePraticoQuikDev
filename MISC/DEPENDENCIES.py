import sqlite3
from APP import db
from os import path, mkdir
from hashlib import sha512
from MISC.CONSTANTS import DB_NAME, ROOT_EMAIL, ROOT_NAME, ROOT_PASSWORD
from APP.Models.users import Users


def createDatabaseIfNotExist():
    if not path.isdir("DATABASES"):
        mkdir("DATABASES")
    if not path.isfile(f"DATABASES/{DB_NAME}"):
        sqlite3.connect(f"DATABASES/{DB_NAME}").close()
        db.create_all()

        rootUser = Users(ROOT_EMAIL, str(sha512(ROOT_PASSWORD.encode()).hexdigest()), ROOT_NAME, "admin")
        db.session.add(rootUser)
        db.session.commit()
