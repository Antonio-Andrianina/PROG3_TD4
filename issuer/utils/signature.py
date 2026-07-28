from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from pathlib import Path
import json
import base64


BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_KEY_PATH = BASE_DIR / "private_key.pem"


def sign_credential(data):

    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = load_pem_private_key(
            f.read(),
            password=None
        )

    payload = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    ).encode()


    signature = private_key.sign(
        payload,
        padding.PKCS1v15(),
        hashes.SHA256()
    )


    return {
        "type": "RSA-SHA256",
        "signature": base64.b64encode(signature).decode()
    }