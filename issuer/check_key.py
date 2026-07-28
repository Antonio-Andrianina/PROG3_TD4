from cryptography.hazmat.primitives import serialization


with open("public_key.pem", "rb") as f:
    key = serialization.load_pem_public_key(
        f.read()
    )


print(type(key))