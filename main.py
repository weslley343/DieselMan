from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.db.database import init_db
from app.application.controllers.user_controller import router as user_router
from app.infrastructure.minio.client import ensure_bucket_exists

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_bucket_exists()  # Garante que o bucket existe
    # await init_db()  # Executa na startup
    yield            # Espera o app rodar
    # (Aqui você pode colocar shutdown se quiser futuramente)

app = FastAPI(title="Clean Architecture Example", lifespan=lifespan)

app.include_router(user_router)