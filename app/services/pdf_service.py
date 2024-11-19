import uuid
from typing import Optional

from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from bson import ObjectId
from io import BytesIO
from datetime import datetime
import PyPDF2

from config import settings
from repositories.pdf_repository import PDFRepository
from models.pdf_document import PDFDocument


class PDFService:
    def __init__(self, repository: PDFRepository = None):
        self.repository = repository or PDFRepository()
        self._client = None
        self._db = None
        self._fs = None

    @property
    def client(self):
        if not self._client:
            self._client = AsyncIOMotorClient(settings.MONGO_URI)
        return self._client

    @property
    def db(self):
        if not self._db:
            self._db = self.client[settings.DATABASE_NAME]
        return self._db

    @property
    def fs(self):
        if not self._fs:
            self._fs = AsyncIOMotorGridFSBucket(self.db)
        return self._fs

    async def upload_pdf(self, file: UploadFile) -> PDFDocument:
        # Read file content
        content = await file.read()

        # Extract metadata from PDF content
        metadata = self._extract_pdf_metadata(BytesIO(content))

        # Generate unique filename
        filename = f"{uuid.uuid4()}_{file.filename}"

        # Store file in GridFS
        file_id = await self.fs.upload_from_stream(
            filename,
            BytesIO(content),  # Pass a stream object
            metadata={
                "content_type": file.content_type or "application/pdf",
                "original_filename": file.filename,
            },
        )

        # Create document model
        pdf_document = PDFDocument(
            filename=file.filename,
            file_id=str(file_id),
            size=len(content),
            content_type=file.content_type or "application/pdf",
            upload_date=datetime.utcnow(),
            metadata=metadata,
        )

        # Save metadata in repository
        return await self.repository.create(pdf_document)

    def _extract_pdf_metadata(self, file_obj: BytesIO) -> dict:
        try:
            reader = PyPDF2.PdfReader(file_obj)
            metadata = reader.metadata or {}
            return {k.replace("/", ""): str(v) for k, v in metadata.items()}
        except Exception:
            return {}

    async def get_pdf_content(self, file_id: str) -> Optional[bytes]:
        try:
            stream = await self.fs.open_download_stream(ObjectId(file_id))
            content = await stream.read()
            await stream.close()
            return content
        except Exception:
            return None

    async def delete_pdf(self, document_id: str) -> bool:
        # Get document to retrieve file_id
        document = await self.repository.get_by_id(document_id)
        if not document:
            return False

        # Delete file from GridFS
        try:
            await self.fs.delete(ObjectId(document.file_id))
        except Exception:
            return False

        # Delete metadata document
        return await self.repository.delete(document_id)
