from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from storage import (
    save_credential,
    get_credential,
    save_verification,
    get_verification_history,
)
from crypto_verify import verify_rsa_signature, verify_jwt_credential


app = FastAPI(title="KYC Verifiable Credential - Offline Verifier")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class CredentialRequest(BaseModel):
    credential: dict


class JWTRequest(BaseModel):
    token: str



@app.get("/")
def home():

    return {
        "status": "KYC Offline Verifier OK",
        "capabilities": [
            "store_credential",
            "verify_rsa_sha256",
            "verify_jwt_es256",
            "verification_history",
        ]
    }



@app.get("/health")
def health():

    return {
        "status": "healthy",
        "mode": "offline",
    }



@app.post("/store")
def store(data: CredentialRequest):

    save_credential(
        data.credential
    )

    return {
        "message": "Verifiable Credential stored"
    }



@app.get("/credential")
def get_wallet_credential():

    return get_credential()



@app.post("/verify")
def verify(data: CredentialRequest):

    result = verify_rsa_signature(data.credential)

    save_verification(result)

    return result



@app.post("/verify-jwt")
def verify_jwt(data: JWTRequest):

    result = verify_jwt_credential(data.token)

    save_verification(result)

    return result



@app.get("/history")
def history():

    return {
        "history": get_verification_history()
    }