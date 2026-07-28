from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path
from datetime import datetime, timezone
import base64
import json


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_PATH = BASE_DIR / "public_key.pem"

with open(PUBLIC_KEY_PATH, "rb") as f:
    RSA_PUBLIC_KEY = serialization.load_pem_public_key(f.read())


REQUIRED_FIELDS = [
    "family_name",
    "given_name",
    "birth_date",
    "birth_place",
    "nationality",
    "resident_address",
    "document_number",
    "issuing_authority",
    "issuing_country",
]


def verify_rsa_signature(credential: dict) -> dict:
    result = {
        "valid": False,
        "checks": {
            "signature": False,
            "required_fields": False,
            "expiration": False,
        },
        "errors": [],
        "credential_type": "RSA-SHA256",
    }

    if "proof" not in credential:
        result["errors"].append("Aucune preuve (proof) dans le Verifiable Credential")
        return result

    proof = credential["proof"]
    if "signature" not in proof:
        result["errors"].append("Aucune signature dans la proof")
        return result

    try:
        signature_bytes = base64.b64decode(proof["signature"])

        unsigned = credential.copy()
        unsigned.pop("proof", None)

        payload = json.dumps(
            unsigned,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

        RSA_PUBLIC_KEY.verify(
            signature_bytes,
            payload,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        result["checks"]["signature"] = True

    except Exception as e:
        result["errors"].append(f"Signature invalide: {str(e)}")
        return result

    subject = credential.get("credentialSubject", {})
    missing = [
        field for field in REQUIRED_FIELDS
        if field not in subject
    ]

    if missing:
        result["errors"].append(f"Champs KYC manquants: {', '.join(missing)}")
        result["checks"]["required_fields"] = False
    else:
        result["checks"]["required_fields"] = True

    if "validUntil" in credential:
        try:
            expiry_str = credential["validUntil"]
            expiry = datetime.fromisoformat(expiry_str)

            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)

            if expiry < datetime.now(timezone.utc):
                result["errors"].append(
                    f"Verifiable Credential expiré depuis le {expiry.strftime('%d/%m/%Y %H:%M')}"
                )
                result["checks"]["expiration"] = False
            else:
                result["checks"]["expiration"] = True

        except Exception as e:
            result["errors"].append(f"Date d'expiration invalide: {str(e)}")
            result["checks"]["expiration"] = False
    else:
        result["checks"]["expiration"] = True

    result["valid"] = all(result["checks"].values())

    if result["valid"]:
        result["issuer"] = credential.get("issuer", {})
        result["subject"] = subject
        result["valid_from"] = credential.get("validFrom")
        result["valid_until"] = credential.get("validUntil")
        result["credential_id"] = credential.get("id")
        result["types"] = credential.get("type", [])

    return result


def verify_jwt_credential(token: str) -> dict:
    try:
        import jwt as pyjwt

        unverified_header = pyjwt.get_unverified_header(token)
        unverified_payload = pyjwt.decode(
            token,
            options={"verify_signature": False}
        )

        result = {
            "valid": False,
            "checks": {
                "signature": False,
                "required_fields": False,
                "expiration": False,
            },
            "errors": [],
            "credential_type": f"JWT-{unverified_header.get('alg', 'unknown')}",
        }

        issuer_did = unverified_payload.get("iss", "")

        if issuer_did.startswith("did:jwk:"):
            jwk_b64 = issuer_did[len("did:jwk:"):]
            padding_needed = 4 - len(jwk_b64) % 4
            if padding_needed != 4:
                jwk_b64 += "=" * padding_needed

            jwk_json = base64.urlsafe_b64decode(jwk_b64)
            jwk_dict = json.loads(jwk_json)

            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.backends import default_backend

            x_bytes = base64.urlsafe_b64decode(
                jwk_dict["x"] + "=" * (4 - len(jwk_dict["x"]) % 4)
            )
            y_bytes = base64.urlsafe_b64decode(
                jwk_dict["y"] + "=" * (4 - len(jwk_dict["y"]) % 4)
            )

            public_numbers = ec.EllipticCurvePublicNumbers(
                x=int.from_bytes(x_bytes, "big"),
                y=int.from_bytes(y_bytes, "big"),
                curve=ec.SECP256R1()
            )
            public_key = public_numbers.public_key(default_backend())

            verified_payload = pyjwt.decode(
                token,
                public_key,
                algorithms=["ES256"],
            )

            result["checks"]["signature"] = True

            vc = verified_payload.get("vc", {})
            subject = vc.get("credentialSubject", {})

            missing = [
                field for field in REQUIRED_FIELDS
                if field not in subject
            ]

            if missing:
                result["errors"].append(f"Champs KYC manquants: {', '.join(missing)}")
            else:
                result["checks"]["required_fields"] = True

            valid_until = vc.get("validUntil")
            if valid_until:
                try:
                    expiry = datetime.fromisoformat(valid_until)
                    if expiry.tzinfo is None:
                        expiry = expiry.replace(tzinfo=timezone.utc)
                    if expiry < datetime.now(timezone.utc):
                        result["errors"].append(
                            f"Verifiable Credential expiré depuis le {expiry.strftime('%d/%m/%Y %H:%M')}"
                        )
                    else:
                        result["checks"]["expiration"] = True
                except Exception:
                    result["checks"]["expiration"] = True
            else:
                result["checks"]["expiration"] = True

            result["valid"] = all(result["checks"].values())

            if result["valid"]:
                result["issuer"] = vc.get("issuer", issuer_did)
                result["subject"] = subject
                result["valid_from"] = vc.get("validFrom")
                result["valid_until"] = valid_until
                result["credential_id"] = vc.get("id")
                result["types"] = vc.get("type", [])

        else:
            result["errors"].append(
                f"Type de DID non supporté: {issuer_did}"
            )

        return result

    except pyjwt.InvalidSignatureError:
        return {
            "valid": False,
            "checks": {"signature": False, "required_fields": False, "expiration": False},
            "errors": ["Signature JWT invalide"],
            "credential_type": "JWT",
        }

    except Exception as e:
        return {
            "valid": False,
            "checks": {"signature": False, "required_fields": False, "expiration": False},
            "errors": [f"Erreur de vérification JWT: {str(e)}"],
            "credential_type": "JWT",
        }
