import datetime
import jwt

class TokenHandler():
    '''
    Helper class with the sole purpose of handling user authorization.
    '''
    @staticmethod
    def get_encoded_token(user, secret_key):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(0, seconds=60*120),
            'iat': datetime.datetime.utcnow(),
            'sub': user
        }
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )

    @staticmethod
    def decode_token(token, secret_key):
        return jwt.decode(token, secret_key)