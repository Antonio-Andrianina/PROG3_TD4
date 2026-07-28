from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import secrets
import time
import json
from urllib.parse import quote

from models import IdentityRequest
from utils.jwt_vc import build_jwt_vc, get_issuer_did


router = APIRouter()


ISSUER_BASE_URL = "http://localhost:8000"  # à remplacer par le domaine public en prod


# Stockage en mémoire pour le MVP (à remplacer par Redis/DB ensuite)
_pre_auth_codes: dict[str, dict] = {}



@router.get("/.well-known/openid-credential-issuer")
def credential_issuer_metadata():

    return {
        "credential_issuer": ISSUER_BASE_URL,
        "credential_endpoint": f"{ISSUER_BASE_URL}/credential",
        "token_endpoint": f"{ISSUER_BASE_URL}/token",

        "credential_configurations_supported": {

            "PersonIdentificationDataKYC": {

                "format": "jwt_vc_json",

                "credential_definition": {
                    "type": [
                        "VerifiableCredential",
                        "PersonIdentificationData"
                    ]
                },

                "cryptographic_binding_methods_supported": [
                    "did:jwk"
                ],

                "credential_signing_alg_values_supported": [
                    "ES256"
                ]
            }
        }
    }




@router.post("/credential-offer")
def create_credential_offer(identity: IdentityRequest):

    code = secrets.token_urlsafe(24)


    _pre_auth_codes[code] = {

        "identity": identity.model_dump(),

        "created_at": time.time(),

        "used": False
    }



    offer = {

        "credential_issuer": ISSUER_BASE_URL,

        "credential_configuration_ids": [
            "PersonIdentificationDataKYC"
        ],

        "grants": {

            "urn:ietf:params:oauth:grant-type:pre-authorized_code": {

                "pre-authorized_code": code

            }
        }
    }



    # JSON valide encodé pour l'URL
    credential_offer_uri = (
            "openid-credential-offer://?credential_offer="
            + quote(json.dumps(offer))
    )


    return {

        "credential_offer": offer,

        "credential_offer_uri": credential_offer_uri

    }




class TokenRequest(BaseModel):

    grant_type: str

    pre_authorized_code: str





@router.post("/token")
def token(req: TokenRequest):

    entry = _pre_auth_codes.get(req.pre_authorized_code)


    if not entry or entry["used"]:

        raise HTTPException(
            status_code=400,
            detail="invalid_grant"
        )



    entry["used"] = True


    access_token = secrets.token_urlsafe(32)


    entry["access_token"] = access_token



    return {

        "access_token": access_token,

        "token_type": "bearer",

        "expires_in": 300

    }





class CredentialApiRequest(BaseModel):

    access_token: str





@router.post("/credential")
def credential(req: CredentialApiRequest):


    match = next(

        (
            e for e in _pre_auth_codes.values()

            if e.get("access_token") == req.access_token

        ),

        None

    )



    if not match:

        raise HTTPException(

            status_code=401,

            detail="invalid_token"

        )



    identity = match["identity"]



    token = build_jwt_vc(

        credential_subject={
            k: v

            for k, v in identity.items()

            if k != "expiry_date"
        },

        vc_type=[
            "PersonIdentificationData"
        ],

        valid_until=identity["expiry_date"]

    )



    return {

        "format": "jwt_vc_json",

        "credential": token

    }