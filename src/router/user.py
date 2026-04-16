#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from typing import List

# Comando que lê os modelos e cria as tabelas no arquivo sghss.db se elas não existirem
models.Base.metadata.create_all(bind=database.engine)

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/user", tags=["Usuário"])

# Função de conexão com o banco
def get_db():
    db = database.SessionLocal() # Abre a conexão
    try:
        yield db # Entrega a conexão para a rota solicitada
    finally:
        db.close() # Fecha a conexão obrigatoriamente ao terminar

# ----- ROTAS PARA USUÁRIOS -----

# Criar usuário e vincular a um perfil. 
@router.post("/usuarios/", response_model=schemas.User)
def criar_usuario(usuario: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o CPF já existe para evitar duplicidade / Se existir, retorna erro 400
    usuario_existente = db.query(models.User).filter(models.User.cpf == usuario.cpf).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    # Adiciona ao db
    db_user = models.User(**usuario.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Lista usuários
@router.get("/usuarios/", response_model=List[schemas.User])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.User).all()