import "./App.css";
import { useState } from "react";
import { QRCodeSVG } from "qrcode.react";
import { createCredentialOffer } from "./api";
import OfflineVerifier from "./components/OfflineVerifier";

function App() {

  const [activeTab, setActiveTab] = useState("verify");

  const [form, setForm] = useState({
    family_name: "",
    given_name: "",
    birth_date: "",
    birth_place: "",
    nationality: "",
    resident_address: "",
    personal_administrative_number: "",
    document_number: "",
    portrait: "",
    expiry_date: "",
    issuing_authority: "",
    issuing_country: "",
  });

  const [offer, setOffer] = useState("");

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit() {
    try {
      const result = await createCredentialOffer({
        ...form,
        nationality: [form.nationality],
      });

      setOffer(result.credential_offer_uri);

    } catch (error) {
      console.error(error);
      alert("Erreur création du Verifiable Credential");
    }
  }

  return (
      <div className="app-shell">

        <header className="app-header">
          <div className="app-header-brand">
            <div className="app-logo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
            </div>
            <div>
              <h1 className="app-title">KYC Verifiable Credentials</h1>
              <p className="app-tagline">EBSI • eIDAS 2.0 • W3C Verifiable Credentials</p>
            </div>
          </div>
          <div className="app-header-badge">
            <span className="status-dot" />
            Offline Ready
          </div>
        </header>

        <nav className="app-tabs">
          <button
            className={`app-tab ${activeTab === "verify" ? "app-tab-active" : ""}`}
            onClick={() => setActiveTab("verify")}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              <polyline points="9 12 11 14 15 10" />
            </svg>
            Vérifier un VC
          </button>
          <button
            className={`app-tab ${activeTab === "issue" ? "app-tab-active" : ""}`}
            onClick={() => setActiveTab("issue")}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="12" y1="18" x2="12" y2="12" />
              <line x1="9" y1="15" x2="15" y2="15" />
            </svg>
            Émettre un VC
          </button>
        </nav>

        <main className="app-content">

          {activeTab === "verify" && (
            <OfflineVerifier />
          )}

          {activeTab === "issue" && (
            <div className="container">

              <form>

                <label>Nom</label>
                <input
                    name="family_name"
                    onChange={handleChange}
                />

                <label>Prénom</label>
                <input
                    name="given_name"
                    onChange={handleChange}
                />

                <label>Date de naissance</label>
                <input
                    type="date"
                    name="birth_date"
                    onChange={handleChange}
                />

                <label>Lieu de naissance</label>
                <input
                    name="birth_place"
                    onChange={handleChange}
                />

                <label>Nationalité</label>
                <input
                    name="nationality"
                    onChange={handleChange}
                />

                <label>Adresse</label>
                <input
                    name="resident_address"
                    onChange={handleChange}
                />

                <label>Numéro document</label>
                <input
                    name="document_number"
                    onChange={handleChange}
                />

                <label>Numéro administratif</label>
                <input
                    name="personal_administrative_number"
                    onChange={handleChange}
                />

                <label>Date expiration</label>
                <input
                    type="date"
                    name="expiry_date"
                    onChange={handleChange}
                />

                <label>Autorité émettrice</label>
                <input
                    name="issuing_authority"
                    onChange={handleChange}
                />

                <label>Pays émission</label>
                <input
                    name="issuing_country"
                    onChange={handleChange}
                />

                <button
                    type="button"
                    onClick={handleSubmit}
                >
                  Générer le Verifiable Credential
                </button>

              </form>

              {offer && (
                  <div className="qr-section">

                    <h3>Scanner avec le Wallet</h3>

                    <div className="qr-box">
                      <QRCodeSVG
                          value={offer}
                          size={250}
                      />
                    </div>

                    <h3>Credential Offer URI :</h3>

                    <p className="offer-text">
                      {offer}
                    </p>

                  </div>
              )}

            </div>
          )}

        </main>

        <footer className="app-footer">
          <span>KYC via Verifiable Credentials</span>
          <span className="app-footer-sep">•</span>
          <span>Vérification offline embarquée</span>
        </footer>

      </div>
  );
}

export default App;