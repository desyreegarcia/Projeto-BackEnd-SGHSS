from fastapi import FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from .models import models, schemas, database # Arquivos internos
from typing import List
from src.router import perfil, user, paciente, medicos, atendimentos

app = FastAPI()

# Comando que lê os modelos e cria as tabelas no arquivo sghss.db se elas não existirem
models.Base.metadata.create_all(bind=database.engine)

# Registro das rotas
app.include_router(perfil.router)
app.include_router(user.router)
app.include_router(paciente.router)
app.include_router(medicos.router)
app.include_router(atendimentos.router)