from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List, Any
from bson import ObjectId
from datetime import datetime
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            if not ObjectId.is_valid(v):
                raise ValueError('Invalid objectid')
            v = ObjectId(v)
        return v

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any,
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                str,
                return_schema=core_schema.str_schema(),
            ),
        )

from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional
from bson import ObjectId

class PDFDocument(BaseModel):
    id: Optional[str] = None
    filename: str
    file_id: str  # GridFS file ID
    size: int
    content_type: str
    upload_date: datetime
    metadata: Dict[str, str]

    class Config:
        json_encoders = {
            ObjectId: str
        }