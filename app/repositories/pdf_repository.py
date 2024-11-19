from motor.motor_asyncio import AsyncIOMotorClient
from models.pdf_document import PDFDocument
from config import settings
from typing import List, Optional

class PDFRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.DATABASE_NAME]
        self.collection = self.db.get_collection("pdfs")

    async def create(self, pdf_document: PDFDocument) -> PDFDocument:
        result = await self.collection.insert_one(pdf_document.dict(by_alias=True))
        pdf_document.id = result.inserted_id
        return pdf_document

    async def get_by_id(self, document_id: str) -> Optional[PDFDocument]:
        document = await self.collection.find_one({"_id": document_id})
        return PDFDocument(**document) if document else None

    async def list_documents(self, skip: int = 0, limit: int = 10) -> List[PDFDocument]:
        cursor = self.collection.find().skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [PDFDocument(**doc) for doc in documents]

    async def update(self, document_id: str, update_data: dict) -> Optional[PDFDocument]:
        result = await self.collection.find_one_and_update(
            {"_id": document_id},
            {"$set": update_data},
            return_document=True
        )
        return PDFDocument(**result) if result else None

    async def delete(self, document_id: str) -> bool:
        result = await self.collection.delete_one({"_id": document_id})
        return result.deleted_count > 0