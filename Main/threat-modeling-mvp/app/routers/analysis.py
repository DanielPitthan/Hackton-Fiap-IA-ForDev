"""
Analysis router — recebe imagem de diagrama e dispara pipeline STRIDE.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/", summary="Submete diagrama para análise STRIDE")
async def analyze_diagram(file: UploadFile = File(...)):
    """
    Recebe uma imagem de diagrama de arquitetura (PNG, JPG, SVG) e retorna
    a análise STRIDE com ameaças e contramedidas identificadas.
    """
    allowed = {"image/png", "image/jpeg", "image/svg+xml"}
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Tipo '{file.content_type}' não suportado. Use PNG, JPEG ou SVG.",
        )

    # TODO: integrar com AnalysisService
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "message": "Arquivo recebido. Análise em processamento.",
            "filename": file.filename,
        },
    )


@router.get("/{analysis_id}", summary="Consulta resultado de uma análise")
async def get_analysis(analysis_id: str):
    """Retorna o resultado de uma análise STRIDE previamente submetida."""
    # TODO: buscar do banco de dados
    return {"analysis_id": analysis_id, "status": "pending"}
