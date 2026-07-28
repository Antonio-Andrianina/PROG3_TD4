from utils.signature import verify_signature


def verify_credential(credential):

    proof = credential.get("proof")


    if not proof:

        return False


    return verify_signature(
        credential,
        proof.get("signature")
    )