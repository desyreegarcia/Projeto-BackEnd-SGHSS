#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from ..models.database import get_db
from typing import List

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

# ----- ROTA PARA PACIENTES -----

# Cadastrar um novo paciente
@router.post("/", response_model=schemas.Paciente)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    
    # Adiciona ao db
    novo_paciente = models.Paciente(**paciente.model_dump())
    db.add(novo_paciente) # Adiciona
    db.commit() # Grava
    db.refresh(novo_paciente) # Atualiza
    return novo_paciente # Retorna

# Listar pacientes cadastrados
@router.get("/", response_model=list[schemas.Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all() # Busca todos os registros e retorna

# Atualizar nome do paciente
@router.put("/{id_user}", response_model=schemas.Paciente)
def atualizar_paciente(id_user: int, paciente_atualizado: schemas.PacienteUpdate, db: Session = Depends(get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id_user == id_user).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não localizado")

    db_paciente.data_nascimento = paciente_atualizado.data_nascimento
    db.commit()
    db.refresh(db_paciente)
    return db_paciente