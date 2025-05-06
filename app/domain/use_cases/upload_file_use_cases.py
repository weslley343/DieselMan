from app.domain.interfaces.file_repository_interface import IFileRepository
from fastapi import UploadFile

class UploadFileUseCase:
    def __init__(self, repository: IFileRepository):
        self.repository = repository

    async def execute(self, file: UploadFile):
        return await self.repository.upload_file(file)
