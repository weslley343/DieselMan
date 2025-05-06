from typing import Protocol

class StorageInterface(Protocol):
    async def upload_file(self, bucket: str, filename: str, content: bytes, content_type: str) -> str:
        """Faz upload de um arquivo e retorna a URL."""
        ...
