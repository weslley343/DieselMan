import io
import mimetypes
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/checklist", tags=["Checklist"])
print("--------------------------------------------")
print("MINIO_ENDPOINT:", os.getenv("MINIO_ENDPOINT"))
print("MINIO_ACCESS_KEY:", os.getenv("MINIO_ACCESS_KEY"))
print("MINIO_SECRET_KEY:", os.getenv("MINIO_SECRET_KEY"))
print("MINIO_BUCKET:", os.getenv("MINIO_BUCKET"))

minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
minio_access_key = os.getenv("MINIO_ACCESS_KEY", "no_access_key")
minio_secret_key = os.getenv("MINIO_SECRET_KEY", "no_secret")
minio_bucket = os.getenv("MINIO_BUCKET", "checklist")

# Instanciando cliente do MinIO (recomendo mover para um módulo separado depois)
minio_client = Minio(
    minio_endpoint,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False,
)

@router.get("/img/{filename}")
async def serve_image(filename: str):
    try:
        
        # Verifica se o arquivo existe no MinIO
        response = minio_client.get_object(bucket_name, filename)

        # Determina o tipo MIME da imagem
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = "application/octet-stream"  # caso não consiga identificar

        # Cria uma resposta com o conteúdo da imagem
        return StreamingResponse(
            io.BytesIO(response.read()),
            media_type=mime_type,
            headers={
                "Content-Disposition": "inline"  # Exibe no navegador
            }
        )

    except S3Error as e:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
@router.post("/add", tags=["Checklist"])
async def create_checklist(file: UploadFile = File(...)):
    try:
        # Cria o bucket se não existir
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        # Salva o arquivo temporariamente
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Faz upload para o MinIO
        minio_client.fput_object(bucket_name, file.filename, temp_path)

        return {"message": f"Arquivo '{file.filename}' enviado com sucesso!"}

    except S3Error as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/add/alotoffiles", tags=["Checklist"])
async def create_checklist(files: List[UploadFile] = File(...)):
    try:
        # Cria o bucket se não existir
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        uploaded_files = []
        for file in files:
            temp_path = f"/tmp/{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(await file.read())

            minio_client.fput_object(
                bucket_name,
                file.filename,
                temp_path
            )

            uploaded_files.append(file.filename)
        return {"message": f"Arquivos enviados com sucesso!"}

    except S3Error as err:
        raise HTTPException(status_code=500, detail=str(err))