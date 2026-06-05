"""
Reports router — geração e download de relatórios de modelagem de ameaças.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/{analysis_id}/pdf", summary="Download do relatório em PDF")
async def download_report_pdf(analysis_id: str):
    """Gera e retorna o relatório STRIDE em PDF para uma análise concluída."""
    # TODO: integrar com ReportService
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Relatório para análise '{analysis_id}' não encontrado.",
    )


@router.get("/{analysis_id}/json", summary="Relatório em JSON")
async def get_report_json(analysis_id: str):
    """Retorna o relatório STRIDE estruturado em JSON."""
    # TODO: buscar do banco de dados
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Relatório para análise '{analysis_id}' não encontrado.",
    )
