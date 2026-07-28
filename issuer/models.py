from pydantic import BaseModel


class IdentityRequest(BaseModel):

    given_name: str

    family_name: str

    birth_date: str

    birth_place: str

    nationality: list[str]

    resident_address: str

    personal_administrative_number: str

    document_number: str

    portrait: str

    expiry_date: str

    issuing_authority: str

    issuing_country: str