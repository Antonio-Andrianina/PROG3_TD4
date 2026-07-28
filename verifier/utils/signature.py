from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from pathlib import Path
import json
import base64


BASE_DIR = Path(__file__).resolve().parent

PUBLIC_KEY_PATH = BASE_DIR / "public_key.pem"



def verify_signature(data, signature):

    with open(PUBLIC_KEY_PATH, "rb") as f:

        public_key = load_pem_public_key(
            f.read()
        )


    clean_data = json.loads(
        json.dumps(data)
    )

    clean_data.pop(
        "proof",
        None
    )


    payload = json.dumps(
        clean_data,
        sort_keys=True,
        separators=(",", ":")
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