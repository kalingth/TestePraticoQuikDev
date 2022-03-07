import re

def validateEmail(email):
    pattern = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(pattern, email):
        return True
    return False
