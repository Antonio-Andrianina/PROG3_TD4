from fastapi import FastAPI
from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

from fastapi.middleware.cors import CORSMiddleware

from models import IdentityRequest
from utils.signature import sign_credential

# Nouveau flux OpenID4VCI
from oid4vci import router as oid4vci_router


app = FastAPI(title="EBSI KYC Issuer")


# Autoriser le frontend React (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



BASE_DIR = Path(__file__).resolve().parent

OUTPUT_PATH = BASE_DIR / "data" / "credential.json"



# Activation du nouveau flux wallet
app.include_router(oid4vci_router)



@app.get("/")
def home():

    return {
        "status": "Issuer OK"
    }



@app.post("/issue")
def issue(identity: IdentityRequest):


    credential = {


        "@context": [

            "https://www.w3.org/ns/credentials/v2"

        ],


        "id":

            f"urn:uuid:{uuid.uuid4()}",



        "type": [

            "VerifiableCredential",

            "PersonIdentificationData"

        ],



        "issuer": {

            "id":

                "did:web:localhost"

        },



        "validFrom":

            datetime.now(
                timezone.utc
            ).isoformat(),



        "validUntil":

            identity.expiry_date,



        "credentialSubject": {


            "family_name":

                identity.family_name,


            "given_name":

                identity.given_name,


            "birth_date":

                identity.birth_date,


            "birth_place":

                identity.birth_place,


            "nationality":

                identity.nationality,


            "resident_address":

                identity.resident_address,


            "personal_administrative_number":

                identity.personal_administrative_number,


            "document_number":

                identity.document_number,


            "portrait":

                identity.portrait,


            "expiry_date":

                identity.expiry_date,


            "issuing_authority":

                identity.issuing_authority,


            "issuing_country":

                identity.issuing_country

        }

    }



    credential["proof"] = sign_credential(
        credential
    )



    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )


    with open(
            OUTPUT_PATH,
            "w",
            encoding="utf-8"
    ) as file:

        json.dump(
            credential,
            file,
            indent=2,
            ensure_ascii=False
        )


    return {

        "message":

            "Credential issued",


        "credential":

            credential

    }