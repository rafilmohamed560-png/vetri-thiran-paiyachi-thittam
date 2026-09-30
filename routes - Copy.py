from fastapi import APIRouter, HTTPException

from backend.config import get_settings
from backend.schemas import DocumentRequest, DocumentResponse
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter(tags=["documents"])


@router.post("/generate", response_model=DocumentResponse)
def generate_document(payload: DocumentRequest) -> DocumentResponse:
    settings = get_settings()
    try:
        generator = GeminiDocumentGenerator(settings)
        content = generator.generate_document(payload)
        return DocumentResponse(
            document_type=payload.document_type,
            content=content,
            model=settings.gemini_model,
            demo_mode=settings.demo_mode,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        # Avoid returning provider credentials or internal tracebacks.
        raise HTTPException(
            status_code=502,
            detail="Document generation failed. Check the server configuration and Gemini API availability.",
        ) from exc
