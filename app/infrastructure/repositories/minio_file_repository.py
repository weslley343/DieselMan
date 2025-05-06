from app.domain.interfaces.file_repository_interface import IFileRepository
from fastapi import UploadFile
from app.infrastructure.minio.client import minio_client, bucket_name
import uuid

class MinioFileRepository(IFileRepository):
    async def upload_file(self, file: UploadFile) -> str:
        file_id = str(uuid.uuid4())  # Gera um ID único para o arquivo
        file_name = f"{file_id}_{file.filename}"  # Nome do arquivo no MinIO
        
        try:
            # Faz o upload do arquivo no MinIO
            minio_client.put_object(
                bucket_name,
                file_name,
                file.file,
                length=file.spool_max_size,
                content_type=file.content_type
            )
            # Retorna a URL pública do arquivo
            file_url = f"http://localhost:9000/{bucket_name}/{file_name}"
            return file_url
        except Exception as e:
            raise Exception(f"Erro ao fazer upload do arquivo: {str(e)}")
