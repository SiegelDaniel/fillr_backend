from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from services.pdf_service import PDFService
from models.pdf_document import PDFDocument
from typing import List

pdf_router = APIRouter(prefix="/pdfs", tags=["PDFs"])

@pdf_router.post("/upload", response_model=PDFDocument)
async def upload_pdf(
    file: UploadFile = File(...),
    service: PDFService = Depends(lambda: PDFService())
):
    return await service.upload_pdf(file)

@pdf_router.get("/", response_model=List[PDFDocument])
async def list_pdfs(
    skip: int = 0,
    limit: int = 10,
    service: PDFService = Depends(lambda: PDFService())
):
    return await service.repository.list_documents(skip, limit)

@pdf_router.get("/{document_id}", response_model=PDFDocument)
async def get_pdf(
    document_id: str,
    service: PDFService = Depends(lambda: PDFService())
):
    document = await service.repository.get_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@pdf_router.delete("/{document_id}")
async def delete_pdf(
    document_id: str,
    service: PDFService = Depends(lambda: PDFService())
):
    deleted = await service.repository.delete(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}
