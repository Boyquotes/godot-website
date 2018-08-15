import os
from werkzeug.security import check_password_hash

def is_valid_user(user):
    """ Check username and credentials
    """
    password_hash = ""
    try:
        password_hash = os.environ["GODOT_USER_" + user['username'].upper()]
    except:
        return False
    return check_password_hash(password_hash, user['password'])


