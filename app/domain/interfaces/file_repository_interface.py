from fastapi import UploadFile
from abc import ABC, abstractmethod

class IFileRepository(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile) -> str:
        """Faz upload do arquivo e retorna a URL"""
        pass
