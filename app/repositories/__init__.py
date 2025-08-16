"""Repository exports."""

from .base import IDocumentRepository
from .mongo_repository import MongoDocumentRepository

__all__ = [
    "IDocumentRepository",
    "MongoDocumentRepository"
]
