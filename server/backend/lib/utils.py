import os
import secrets
import string
from base64 import b64decode, b64encode
import uuid


def generate_random_string(size_of_str: int) -> str:
    chars = string.ascii_lowercase + string.digits
    # To prevent “bad words”, remove vowels and the numbers 0,1 and 3
    for char in "aeiou013":
        chars = chars.replace(char, "")
    random_str = "".join(secrets.choice(chars) for _ in range(size_of_str))
    return random_str


def base64_encoder_decoder(data: str, to_encode: bool = False) -> str:
    data_bytes = str(data).encode("ascii")

    if to_encode:
        base64_bytes = b64encode(data_bytes)
    else:
        base64_bytes = b64decode(data_bytes)

    resp_data = base64_bytes.decode("ascii")

    return resp_data


def uuid_gen(name: str):
    return uuid.uuid5(namespace=uuid.UUID(str(os.getenv("UUID_NAMESPACE"))), name=name)
