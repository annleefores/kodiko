import time
import os
import requests
from requests import ConnectionError
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode

# Download public keys
try:
    response = requests.get(
        f'https://cognito-idp.{os.getenv("REGION")}.amazonaws.com/{os.getenv("COGNITO_USER_POOL_ID")}/.well-known/jwks.json'
    )
except ConnectionError as e:
    raise Exception("Connection Error, Unable to download jwks", str(e))


keys = response.json()["keys"]


class CognitoJwtToken:
    def __init__(self, token: str) -> None:
        self.bearer_token = token
        self.token = ""
        self.key = None

    def check_auth_type(self):
        type, token = self.bearer_token.split(" ")

        if type != "Bearer":
            raise Exception("Token type must be Bearer")

        self.token = token

    def public_key(self):
        # get the kid from the token header
        try:
            headers = jwt.get_unverified_headers(token=self.token)
        except JOSEError as e:
            raise Exception(str(e)) from e

        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(keys)):
            if kid == keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise Exception("Public key not found in jwks.json")
        try:
            # construct the public key
            self.key = jwk.construct(keys[key_index])
        except JOSEError as e:
            raise Exception(str(e)) from e

    def verify_signature(self):
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(self.token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if self.key is not None:
            if not self.key.verify(msg=message.encode("utf8"), sig=decoded_signature):
                raise Exception("Signature verification failed")

    def return_verified_claim(self):
        try:
            claims = jwt.get_unverified_claims(self.token)
        except JOSEError as e:
            raise Exception(str(e)) from e

        # additionally we can verify the token expiration
        if time.time() > claims["exp"]:
            raise Exception("Token is expired")

        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != os.getenv("COGNITO_CLIENT_ID"):
            raise Exception("Token was not issued for this audience")

        return claims

    def verify(self):
        self.check_auth_type()
        self.public_key()
        self.verify_signature()
        claims = self.return_verified_claim()
        return claims
