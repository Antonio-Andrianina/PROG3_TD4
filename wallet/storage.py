from pathlib import Path
import json
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parent

FILE = BASE_DIR / "wallet.json"

HISTORY_FILE = BASE_DIR / "verification_history.json"



def save_credential(credential):

    with open(
            FILE,
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            credential,
            f,
            indent=2,
            ensure_ascii=False
        )



def get_credential():

    if not FILE.exists():

        return {
            "error": "No credential available"
        }


    with open(
            FILE,
            "r",
            encoding="utf-8"
    ) as f:

        return json.load(f)



def save_verification(result):

    history = get_verification_history()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "valid": result.get("valid", False),
        "credential_type": result.get("credential_type", "unknown"),
        "credential_id": result.get("credential_id"),
        "issuer": result.get("issuer"),
        "errors": result.get("errors", []),
    }

    subject = result.get("subject", {})
    if subject:
        entry["subject_name"] = (
            f"{subject.get('given_name', '')} {subject.get('family_name', '')}"
        ).strip()

    history.insert(0, entry)

    history = history[:50]

    with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=2,
            ensure_ascii=False
        )



def get_verification_history():

    if not HISTORY_FILE.exists():
        return []

    try:
        with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
        ) as f:
            return json.load(f)

    except (json.JSONDecodeError, Exception):
        return []