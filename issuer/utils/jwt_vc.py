import jwt
import uuid
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

from .did_jwk import did_jwk_from_public_key

BASE_DIR = Path(__file__).resolve().parent.parent
EC_PRIVATE_KEY_PATH = BASE_DIR / "ec_private_key.pem"
EC_PUBLIC_KEY_PATH = BASE_DIR / "ec_public_key.pem"


def _load_ec_private_key():
    with open(EC_PRIVATE_KEY_PATH, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


def _load_ec_public_key():
    with open(EC_PUBLIC_KEY_PATH, "rb") as f:
        return load_pem_public_key(f.read())


def get_issuer_did() -> str:
    return did_jwk_from_public_key(_load_ec_public_key())


def build_jwt_vc(credential_subject: dict, vc_type: list[str], valid_until: str) -> str:
    """Construit et signe une VC au format jwt_vc_json (ES256), sans toucher au flux RSA existant."""
    issuer_did = get_issuer_did()
    now = datetime.now(timezone.utc)
    credential_id = f"urn:uuid:{uuid.uuid4()}"

    vc_payload = {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "id": credential_id,
        "type": ["VerifiableCredential"] + vc_type,
        "issuer": issuer_did,
        "validFrom": now.isoformat(),
        "validUntil": valid_until,
        "credentialSubject": credential_subject,
    }

    jwt_claims = {
        "iss": issuer_did,
        "iat": int(now.timestamp()),
        "jti": credential_id,
        "vc": vc_payload,
    }

    private_key = _load_ec_private_key()
    headers = {"typ": "JWT", "kid": f"{issuer_did}#0"}

    token = jwt.encode(jwt_claims, private_key, algorithm="ES256", headers=headers)
    return token