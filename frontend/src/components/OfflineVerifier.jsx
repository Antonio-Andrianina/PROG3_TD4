import { useState, useRef } from "react";
import { verifyCredentialOffline, verifyJWTOffline } from "../api";
import VerificationResult from "./VerificationResult";

export default function OfflineVerifier() {
    const [jsonInput, setJsonInput] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [error, setError] = useState("");
    const fileInputRef = useRef(null);

    async function handleVerify() {
        if (!jsonInput.trim()) {
            setError("Veuillez coller un Verifiable Credential (JSON ou JWT)");
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {
            const trimmed = jsonInput.trim();

            const isJWT = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(trimmed);

            let verificationResult;

            if (isJWT) {
                verificationResult = await verifyJWTOffline(trimmed);
            } else {
                let credential;
                try {
                    credential = JSON.parse(trimmed);
                } catch {
                    setError("JSON invalide. Vérifiez le format du Verifiable Credential.");
                    setLoading(false);
                    return;
                }
                verificationResult = await verifyCredentialOffline(credential);
            }

            setResult(verificationResult);

        } catch (err) {
            setError(
                "Erreur de connexion au vérificateur. " +
                "Vérifiez que le service wallet est lancé (port 8002)."
            );
        } finally {
            setLoading(false);
        }
    }

    function handleDrag(e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    }

    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        const files = e.dataTransfer.files;
        if (files && files[0]) {
            readFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        if (files && files[0]) {
            readFile(files[0]);
        }
    }

    function readFile(file) {
        if (!file.name.endsWith(".json") && !file.name.endsWith(".jwt") && !file.name.endsWith(".txt")) {
            setError("Format non supporté. Utilisez un fichier .json, .jwt ou .txt");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            setJsonInput(e.target.result);
            setError("");
            setResult(null);
        };
        reader.readAsText(file);
    }

    function handleClear() {
        setJsonInput("");
        setResult(null);
        setError("");
    }

    function handleLoadExample() {
        const example = JSON.stringify({
            "@context": ["https://www.w3.org/ns/credentials/v2"],
            "id": "urn:uuid:example-test",
            "type": ["VerifiableCredential", "PersonIdentificationData"],
            "issuer": { "id": "did:web:localhost" },
            "validFrom": "2025-01-01T00:00:00+00:00",
            "validUntil": "2030-12-31T23:59:59+00:00",
            "credentialSubject": {
                "family_name": "Dupont",
                "given_name": "Jean",
                "birth_date": "1990-05-15",
                "birth_place": "Paris",
                "nationality": ["FR"],
                "resident_address": "123 Rue de la Paix, Paris",
                "document_number": "ABC123456",
                "issuing_authority": "Préfecture de Paris",
                "issuing_country": "FR"
            },
            "proof": {
                "type": "RSA-SHA256",
                "signature": "EXEMPLE_SIGNATURE_NON_VALIDE"
            }
        }, null, 2);
        setJsonInput(example);
        setError("");
        setResult(null);
    }

    return (
        <div className="ov-container">
            <div className="ov-header">
                <div className="ov-header-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        <polyline points="9 12 11 14 15 10" />
                    </svg>
                </div>
                <div>
                    <h2 className="ov-title">Vérificateur KYC Offline</h2>
                    <p className="ov-subtitle">
                        Vérification de Verifiable Credentials sans connexion réseau
                    </p>
                </div>
            </div>

            <div
                className={`ov-dropzone ${dragActive ? "ov-dropzone-active" : ""}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".json,.jwt,.txt"
                    onChange={handleFileSelect}
                    style={{ display: "none" }}
                />
                <div className="ov-dropzone-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                </div>
                <p className="ov-dropzone-text">
                    Glissez un Verifiable Credential ici ou cliquez pour importer
                </p>
                <p className="ov-dropzone-hint">
                    .json • .jwt • .txt
                </p>
            </div>

            <div className="ov-input-section">
                <div className="ov-input-header">
                    <span className="ov-input-label">Ou collez le Verifiable Credential ici</span>
                    <div className="ov-input-actions">
                        <button
                            className="ov-btn-ghost"
                            onClick={handleLoadExample}
                            title="Charger un exemple de VC"
                        >
                            Exemple
                        </button>
                        {jsonInput && (
                            <button
                                className="ov-btn-ghost"
                                onClick={handleClear}
                            >
                                Effacer
                            </button>
                        )}
                    </div>
                </div>
                <textarea
                    className="ov-textarea"
                    value={jsonInput}
                    onChange={(e) => {
                        setJsonInput(e.target.value);
                        setError("");
                    }}
                    placeholder='{"@context": [...], "type": ["VerifiableCredential", "PersonIdentificationData"], "credentialSubject": {...}, "proof": {...}}'
                    rows={8}
                    spellCheck={false}
                />
            </div>

            {error && (
                <div className="ov-error">
                    <span className="ov-error-icon">⚠</span>
                    <span>{error}</span>
                </div>
            )}

            <button
                className={`ov-verify-btn ${loading ? "ov-verify-loading" : ""}`}
                onClick={handleVerify}
                disabled={loading || !jsonInput.trim()}
            >
                {loading ? (
                    <>
                        <span className="ov-spinner" />
                        Vérification KYC en cours...
                    </>
                ) : (
                    <>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="20" height="20">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        </svg>
                        Vérifier le Verifiable Credential
                    </>
                )}
            </button>

            <VerificationResult result={result} />
        </div>
    );
}
