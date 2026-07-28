import { useState } from "react";

export default function VerificationResult({ result }) {
    const [showDetails, setShowDetails] = useState(false);

    if (!result) return null;

    const isValid = result.valid;
    const checks = result.checks || {};
    const errors = result.errors || [];
    const subject = result.subject || {};

    return (
        <div className={`vr-container ${isValid ? "vr-valid" : "vr-invalid"}`}>

            <div className={`vr-badge ${isValid ? "vr-badge-valid" : "vr-badge-invalid"}`}>
                <div className="vr-badge-icon">
                    {isValid ? (
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                            <polyline points="22 4 12 14.01 9 11.01" />
                        </svg>
                    ) : (
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10" />
                            <line x1="15" y1="9" x2="9" y2="15" />
                            <line x1="9" y1="9" x2="15" y2="15" />
                        </svg>
                    )}
                </div>
                <h2 className="vr-badge-title">
                    {isValid ? "KYC Credential Vérifié" : "KYC Credential Invalide"}
                </h2>
                <p className="vr-badge-subtitle">
                    {isValid
                        ? "Verifiable Credential vérifié offline avec succès"
                        : errors[0] || "La vérification du Verifiable Credential a échoué"
                    }
                </p>
                <span className="vr-badge-type">{result.credential_type}</span>
            </div>

            <div className="vr-checks">
                <div className={`vr-check ${checks.signature ? "vr-check-pass" : "vr-check-fail"}`}>
                    <span className="vr-check-icon">{checks.signature ? "✓" : "✗"}</span>
                    <span>Signature cryptographique</span>
                </div>
                <div className={`vr-check ${checks.required_fields ? "vr-check-pass" : "vr-check-fail"}`}>
                    <span className="vr-check-icon">{checks.required_fields ? "✓" : "✗"}</span>
                    <span>Attributs KYC obligatoires</span>
                </div>
                <div className={`vr-check ${checks.expiration ? "vr-check-pass" : "vr-check-fail"}`}>
                    <span className="vr-check-icon">{checks.expiration ? "✓" : "✗"}</span>
                    <span>Validité temporelle</span>
                </div>
            </div>

            {errors.length > 0 && (
                <div className="vr-errors">
                    {errors.map((err, i) => (
                        <div key={i} className="vr-error-item">
                            <span className="vr-error-icon">⚠</span>
                            <span>{err}</span>
                        </div>
                    ))}
                </div>
            )}

            {isValid && Object.keys(subject).length > 0 && (
                <div className="vr-id-card">
                    <div className="vr-id-header">
                        <div className="vr-id-flag">🇪🇺</div>
                        <div>
                            <h3 className="vr-id-title">Données KYC vérifiées</h3>
                            <p className="vr-id-subtitle">PersonIdentificationData — eIDAS 2.0</p>
                        </div>
                    </div>

                    <div className="vr-id-grid">
                        {subject.family_name && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Nom</span>
                                <span className="vr-id-value">{subject.family_name}</span>
                            </div>
                        )}
                        {subject.given_name && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Prénom</span>
                                <span className="vr-id-value">{subject.given_name}</span>
                            </div>
                        )}
                        {subject.birth_date && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Date de naissance</span>
                                <span className="vr-id-value">{subject.birth_date}</span>
                            </div>
                        )}
                        {subject.birth_place && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Lieu de naissance</span>
                                <span className="vr-id-value">{subject.birth_place}</span>
                            </div>
                        )}
                        {subject.nationality && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Nationalité</span>
                                <span className="vr-id-value">
                                    {Array.isArray(subject.nationality)
                                        ? subject.nationality.join(", ")
                                        : subject.nationality
                                    }
                                </span>
                            </div>
                        )}
                        {subject.resident_address && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Adresse</span>
                                <span className="vr-id-value">{subject.resident_address}</span>
                            </div>
                        )}
                        {subject.document_number && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">N° Document</span>
                                <span className="vr-id-value">{subject.document_number}</span>
                            </div>
                        )}
                        {subject.issuing_authority && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Autorité</span>
                                <span className="vr-id-value">{subject.issuing_authority}</span>
                            </div>
                        )}
                        {subject.issuing_country && (
                            <div className="vr-id-field">
                                <span className="vr-id-label">Pays</span>
                                <span className="vr-id-value">{subject.issuing_country}</span>
                            </div>
                        )}
                    </div>

                    <div className="vr-id-dates">
                        {result.valid_from && (
                            <div className="vr-id-date">
                                <span className="vr-id-label">Émis le</span>
                                <span className="vr-id-value">
                                    {new Date(result.valid_from).toLocaleDateString("fr-FR")}
                                </span>
                            </div>
                        )}
                        {result.valid_until && (
                            <div className="vr-id-date">
                                <span className="vr-id-label">Valide jusqu'au</span>
                                <span className="vr-id-value">
                                    {new Date(result.valid_until).toLocaleDateString("fr-FR")}
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            )}

            <button
                className="vr-details-toggle"
                onClick={() => setShowDetails(!showDetails)}
            >
                {showDetails ? "Masquer" : "Détails techniques"}
                <span className={`vr-arrow ${showDetails ? "vr-arrow-up" : ""}`}>▼</span>
            </button>

            {showDetails && (
                <div className="vr-details">
                    {result.credential_id && (
                        <div className="vr-detail-row">
                            <span className="vr-detail-label">ID</span>
                            <span className="vr-detail-value">{result.credential_id}</span>
                        </div>
                    )}
                    {result.issuer && (
                        <div className="vr-detail-row">
                            <span className="vr-detail-label">Issuer</span>
                            <span className="vr-detail-value">
                                {typeof result.issuer === "object"
                                    ? result.issuer.id || JSON.stringify(result.issuer)
                                    : result.issuer
                                }
                            </span>
                        </div>
                    )}
                    {result.types && (
                        <div className="vr-detail-row">
                            <span className="vr-detail-label">Types</span>
                            <span className="vr-detail-value">{result.types.join(", ")}</span>
                        </div>
                    )}
                    <div className="vr-detail-row">
                        <span className="vr-detail-label">Algo</span>
                        <span className="vr-detail-value">{result.credential_type}</span>
                    </div>
                    <div className="vr-detail-row">
                        <span className="vr-detail-label">Mode</span>
                        <span className="vr-detail-value">Vérification 100% offline</span>
                    </div>
                </div>
            )}
        </div>
    );
}
