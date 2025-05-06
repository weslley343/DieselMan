from fastapi import APIRouter, UploadFile, File, HTTPException
from app.domain.use_cases.upload_file_use_cases import UploadFileUseCase
from app.infrastructure.repositories.minio_file_repository import MinioFileRepository

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Inicializa o repositório e o use case
    repository = MinioFileRepository()
    use_case = UploadFileUseCase(repository)

    try:
        # Lê o conteúdo do arquivo de forma assíncrona
        file_content = await file.read()

        # Chama o use case para fazer o upload
        file_url = await use_case.execute(file.filename)

        return {"file_url": file_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload do arquivo: {str(e)}")
