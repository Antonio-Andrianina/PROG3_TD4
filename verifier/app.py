from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import json
from datetime import datetime, timezone


app = FastAPI(title="Offline KYC Verifier")


BASE_DIR = Path(__file__).resolve().parent

PUBLIC_KEY_PATH = BASE_DIR / "public_key.pem"


with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = serialization.load_pem_public_key(
        f.read()
    )


class CredentialRequest(BaseModel):
    credential: dict



@app.get("/")
def home():
    return {
        "status": "Verifier Offline OK"
    }



@app.post("/verify")
def verify(data: CredentialRequest):

    credential = data.credential


    if "proof" not in credential:
        return {
            "valid": False,
            "error": "Missing proof"
        }


    try:

        signature = base64.b64decode(
            credential["proof"]["signature"]
        )


        unsigned = credential.copy()

        unsigned.pop(
            "proof",
            None
        )


        payload = json.dumps(
            unsigned,
            sort_keys=True,
            separators=(",", ":")
        ).encode()



        PUBLIC_KEY.verify(

            signature,

            payload,

            padding.PKCS1v15(),

            hashes.SHA256()

        )



        required_fields = [
            "family_name",
            "given_name",
            "birth_date",
            "birth_place",
            "nationality",
            "resident_address",
            "document_number",
            "issuing_authority",
            "issuing_country"
        ]


        subject = credential.get(
            "credentialSubject",
            {}
        )


        missing = [
            field
            for field in required_fields
            if field not in subject
        ]


        if missing:
            return {
                "valid": False,
                "error": "Missing attributes",
                "fields": missing
            }



        if "validUntil" in credential:

            expiry = datetime.fromisoformat(
                credential["validUntil"]
            ).replace(
                tzinfo=timezone.utc
            )


            if expiry < datetime.now(timezone.utc):

                return {
                    "valid": False,
                    "error": "Credential expired"
                }



        return {

            "valid": True,

            "issuer": credential.get(
                "issuer"
            ),

            "subject": subject,

            "message":
                "Credential verified offline"

        }



    except Exception as e:

        return {

            "valid": False,

            "message":
                "Invalid signature",

            "detail":
                str(e)

        }