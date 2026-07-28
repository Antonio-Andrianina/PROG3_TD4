import base64
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def public_key_to_jwk(public_key: ec.EllipticCurvePublicKey) -> dict:
    numbers = public_key.public_numbers()
    size = (public_key.curve.key_size + 7) // 8
    x = numbers.x.to_bytes(size, "big")
    y = numbers.y.to_bytes(size, "big")
    return {
        "kty": "EC",
        "crv": "P-256",
        "x": _b64url(x),
        "y": _b64url(y),
    }


def did_jwk_from_public_key(public_key: ec.EllipticCurvePublicKey) -> str:
    jwk = public_key_to_jwk(public_key)
    encoded = _b64url(json.dumps(jwk, separators=(",", ":")).encode())
    return f"did:jwk:{encoded}"