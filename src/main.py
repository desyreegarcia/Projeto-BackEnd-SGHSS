from fastapi import FastAPI
from .models.database import engine, Base
from .models import models

# Cria as tabelas no sghss.db ao iniciar o servidor
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SGHSS",
    description="Sistema de Gestão Hospitalar e de Serviços de Saúde",
    version="1.0.0"
)

@app.get("/", tags=["Home"])
def read_root():
    return {
        "mensagem": "Bem-vindo à API do Sistema de Gestão Hospitalar e de Serviços de Saúde",
        "status": "Online",
        "documentacao": "/docs"
    }

@app.get("/saude", tags=["Monitoramento"])
def check_health():
    return {"status": "Sistema operacional", "database": "SQLite Conectado"}