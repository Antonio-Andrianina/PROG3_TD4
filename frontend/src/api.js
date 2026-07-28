const ISSUER_URL = "http://localhost:8000";
const WALLET_URL = "http://localhost:8002";


export async function issueCredential(identity) {
    const response = await fetch(
        `${ISSUER_URL}/issue`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(identity),
        }
    );
    if (!response.ok) throw new Error("Erreur émission du credential");
    const data = await response.json();
    return data.credential;
}


export async function fetchJwtCredential(preAuthCode) {
    const tokenRes = await fetch(`${ISSUER_URL}/token`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            grant_type: "urn:ietf:params:oauth:grant-type:pre-authorized_code",
            pre_authorized_code: preAuthCode,
        }),
    });
    if (!tokenRes.ok) throw new Error("Erreur token OID4VCI");
    const { access_token } = await tokenRes.json();

    const credRes = await fetch(`${ISSUER_URL}/credential`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ access_token }),
    });
    if (!credRes.ok) throw new Error("Erreur récupération credential JWT");
    const { credential } = await credRes.json();
    return credential;
}


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