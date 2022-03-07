from time import time
from EndpointTests.usersCRU import testUserCreateReadUpdate
from EndpointTests.postsCRU import testPostCreateReadUpdateUpload
from EndpointTests.commentCRU import testCommentCreateReadUpdate
from EndpointTests.deleteRoutine import completeDeleteRoutine
from EndpointTests.adminScope import testAdminScope


def rotina_completa():
    # O usuário admin é criado atraves do path MISC/DEPENDENCIES caso não haja nenhum banco de dados
    admin = {"email": "root@domain.com", "password": "root"}
    # Usuários para Teste. Na seção de comentários, o usuário 1 será notificado por email.
    # É importante colocar seu email real para verificar o recebimento do email.
    users = [
        {"email": "wallace.u8@gmail.com", "password": "p@ssw0rd", "name": "Wallace Rocha Faria"},
        {"email": "wallace13@hotmail.com.br", "password": "senha123", "name": "Wallace R. Faria"}
    ]
    startAt = time()
    testUserCreateReadUpdate(users)
    testPostCreateReadUpdateUpload(users)
    testCommentCreateReadUpdate(users)
    testAdminScope(users[0], admin)
    completeDeleteRoutine(users)
    timer = int(time() - startAt)
    hours, minutes, seconds = timer // 3600, (timer % 3600) // 60, timer % 60
    print("-"*102, "Este teste demorou: {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), sep="\n")


if __name__ == "__main__":
    rotina_completa()
