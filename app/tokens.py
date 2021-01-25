from jwt import decode, encode
from time import time
from app.select_dao import SelectDAO

secret_key = "you-will-never-guess"


def get_reset_password_token(user, expires_in=600):
    return encode(
        {
            'reset_password': user.id,
            'exp': time() + expires_in
        },
        secret_key,
        algorithm='HS256'
    )


def verify_reset_password_token(token):
    try:
        user_id = decode(
            token,
            secret_key,
            algorithms=['HS256']
        )['reset_password']
    except:
        return
    return SelectDAO.select_user_by_id(user_id)
