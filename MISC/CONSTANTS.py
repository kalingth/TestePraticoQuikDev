from os import path
from uuid import uuid4


class Messages:
    SUCCESS_MESSAGE = "Done!"
    UNAUTHORIZATED = "You're unauthorizated to reach that resource!"
    DEFAULT_SERVER_ERROR = "Your request has not been processed properly."
    RESOURCE_NOT_FOUND = "You're trying to get/edit a resource that not exists!"
    RESOURCE_NOT_REACHABLE = "You're trying to edit a resource that you can't edit!"
    ATTRIBUTE_NOT_FOUND = "Your request seems incomplete!"


ROOT_EMAIL = "root@domain.com"
ROOT_NAME = "Super User"
ROOT_PASSWORD = "root"

with open("MISC/MailTemplate.html") as file:
    MAIL_TEMPLATE = file.read()

MAILJET_API_KEY = '900dcabc73886509be057eef39f22fc8'
MAILJET_API_SECRET = 'Por favor, me contate para que eu forneça esta chave'
HOST = "0.0.0.0"
MAIN_PORT = 5000
DB_NAME = "persistQuik.db"
KEY = uuid4().hex
PATH = path.join(path.pardir, "DATABASES", DB_NAME)

