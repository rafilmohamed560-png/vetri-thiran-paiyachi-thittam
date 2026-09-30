from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=2, max_length=4000)
    terms: str = Field(min_length=2, max_length=8000)
    effective_date: str = Field(min_length=2, max_length=100)
    extra_instructions: str = Field(default="", max_length=4000)

    @field_validator("document_type", "parties", "terms", "effective_date", "extra_instructions")
    @classmethod
    def strip_values(cls, value: str) -> str:
        return value.strip()


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    demo_mode: bool
