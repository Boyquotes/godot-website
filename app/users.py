import os


def is_valid_user(user):
    """ Check username and credentials
    """
    password = None
    try:
        password = os.environ["GODOT_USER_" + user['username'].upper()]
    except:
        return False
    if user['password'] == password:
        return True
    return False
