import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask import Flask, jsonify


AUTH0_DOMAIN = 'dev-6gnrncvpus8amyed.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'places'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        abort(401)

    elif len(parts) == 1:
        abort(401)

    elif len(parts) > 2:
        abort(401)
    token = parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(403)

    if permission not in payload['permissions']:
        abort(403)
    return True

def verify_decode_jwt(token):
    try:
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
    except:
        abort(401)
    if 'kid' not in unverified_header:
        abort(401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except:
            abort(401)

def get_user_id(payload):
    return payload.get('sub').split('|')[1]

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            user_id = get_user_id(payload)
            check_permissions(permission, payload)
            return f(user_id, *args, **kwargs)

        return wrapper
    return requires_auth_decorator