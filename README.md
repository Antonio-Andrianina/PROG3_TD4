# KYC Verifiable Credential

## Services

Issuer:
- Création et signature des Verifiable Credentials

Verifier:
- Vérification de la signature

Wallet:
- Stockage du Credential

## Lancement

Issuer:

cd issuer
uvicorn app:app --reload


Verifier:

cd verifier
uvicorn main:app --port 8001 --reload


Wallet:

cd wallet
uvicorn main:app --port 8002 --reload


## Flow

1. L'utilisateur fournit ses informations.
2. Issuer crée un VC.
3. Issuer signe avec sa clé privée.
4. Wallet stocke le VC.
5. Verifier vérifie avec la clé publique.