#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from typing import List

# Comando que lê os modelos e cria as tabelas no arquivo sghss.db se elas não existirem
models.Base.metadata.create_all(bind=database.engine)

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/medicos", tags=["Médicos"])

# Função de conexão com o banco
def get_db():
    db = database.SessionLocal() # Abre a conexão
    try:
        yield db # Entrega a conexão para a rota solicitada
    finally:
        db.close() # Fecha a conexão obrigatoriamente ao terminar

# ----- MÉDICOS -----

# Cadastrar um novo médico
@router.post("/medicos/", response_model=schemas.Medico)
def criar_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    # Verifica se o Registro Profissional já existe / Se existir, retorna erro 400
    db_medico = db.query(models.Medico).filter(models.Medico.registro_profissional == medico.registro_profissional).first()
    if db_medico:
        raise HTTPException(status_code=400, detail="Médico já cadastrado com este registro")
    
    # Adiciona ao db
    novo_medico = models.Medico(**medico.model_dump())
    db.add(novo_medico)
    db.commit()
    db.refresh(novo_medico)
    return novo_medico

# Listar todos os médicos
@router.get("/medicos/", response_model=list[schemas.Medico])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(models.Medico).all()

# Atualizar nome do medico
@router.put("/{id_user}", response_model=schemas.Medico)
def atualizar_medico(id_user: str, medico_atualizado: schemas.MedicoUpdate, db: Session = Depends(get_db)):
    db_medico = db.query(models.Medico).filter(models.Medico.id_user == id_user).first()
    
    '''if not db_paciente:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Usuário não localizado")'''

    db_medico.especialidade = medico_atualizado.especialidade
    db.commit()
    db.refresh(db_medico)
    return db_medico