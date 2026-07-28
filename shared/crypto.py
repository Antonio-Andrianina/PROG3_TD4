from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key
)
from pathlib import Path
import base64
import json


def sign_data(data, private_key_path):

    with open(
            private_key_path,
            "rb"
    ) as f:

        private_key = load_pem_private_key(
            f.read(),
            password=None
        )


    payload = json.dumps(
        data,
        sort_keys=True
    ).encode()


    signature = private_key.sign(

        payload,

        padding.PKCS1v15(),

        hashes.SHA256()

    )


    return base64.b64encode(
        signature
    ).decode()



def verify_data(data, signature, public_key_path):

    with open(
            public_key_path,
            "rb"
    ) as f:

        public_key = load_pem_public_key(
            f.read()
        )


    payload = json.dumps(
        data,
        sort_keys=True
    ).encode()


    try:

        public_key.verify(

            base64.b64decode(signature),

            payload,

            padding.PKCS1v15(),

            hashes.SHA256()

        )

        return True


    except Exception:

        return False