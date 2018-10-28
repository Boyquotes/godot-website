import os
from werkzeug.security import check_password_hash

def is_valid_user(user):
    """ Check username and credentials
    """
    password_hash = ""
    try:
        password_hash = os.environ["GODOT_USER_" + user['username'].upper().strip()]
        return check_password_hash(password_hash, user['password'])
    except:
        return False


def get_user_full_name(user):
    """ get user's full name from OS ENV """
    full_name = ""
    try:
        full_name = os.environ["GODOT_USER_" + user['username'].upper().strip() + "_FULLNAME"]
        return full_name
    except:
        return full_name


def get_user_project_name(user):
    """ get user's project name from OS ENV """
    project_name = ""
    try:
        project_name = os.environ["GODOT_USER_" + user['username'].upper().strip() + "_PROJECT_NAME"]
        return project_name
    except:
        return project_name


def get_user_project_description_uri(user):
    """ get user's project description URI from OS ENV """
    project_description_uri = ""
    try:
        project_description_uri = os.environ["GODOT_USER_" + user['username'].upper().strip() + "_PROJECT_DESCRIPTION_URI"]
        return project_description_uri
    except:
        return project_description_uri
