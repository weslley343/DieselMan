from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv()

# Verificar se as variáveis de ambiente estão corretas
# print("MINIO_ENDPOINT:", os.getenv("MINIO_ENDPOINT"))
# print("MINIO_ACCESS_KEY:", os.getenv("MINIO_ACCESS_KEY"))
# print("MINIO_SECRET_KEY:", os.getenv("MINIO_SECRET_KEY"))
# print("MINIO_BUCKET:", os.getenv("MINIO_BUCKET"))

minio_client = Minio(
    "localhost:9000",
    access_key="hySXA7wwxM3QTJpuVBgf",
    secret_key="pkvTUP5Mxx6yuxK4fOGRnAnVhRAy1TWUIQvErKzY",
    secure=False,
)

bucket_name = os.getenv("MINIO_BUCKET", "scenes-files")

def ensure_bucket_exists():
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
