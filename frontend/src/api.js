const ISSUER_URL = "http://localhost:8000";
const WALLET_URL = "http://localhost:8002";


export async function createCredentialOffer(identity) {
    const response = await fetch(
        `${ISSUER_URL}/credential-offer`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(identity),
        }
    );

    if (!response.ok) {
        throw new Error("Erreur issuer");
    }

    return await response.json();
}


export async function verifyCredentialOffline(credential) {
    const response = await fetch(
        `${WALLET_URL}/verify`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ credential }),
        }
    );

    if (!response.ok) {
        throw new Error("Erreur vérification");
    }

    return await response.json();
}


export async function verifyJWTOffline(token) {
    const response = await fetch(
        `${WALLET_URL}/verify-jwt`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token }),
        }
    );

    if (!response.ok) {
        throw new Error("Erreur vérification JWT");
    }

    return await response.json();
}


export async function getVerificationHistory() {
    const response = await fetch(`${WALLET_URL}/history`);

    if (!response.ok) {
        throw new Error("Erreur historique");
    }

    return await response.json();
}