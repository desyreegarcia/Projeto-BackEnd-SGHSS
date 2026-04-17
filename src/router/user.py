#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from typing import List

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/user", tags=["Usuário"])

# Função de conexão com o banco
def get_db():
    db = database.SessionLocal() # Abre a conexão
    try:
        yield db # Entrega a conexão para a rota solicitada
    finally:
        db.close() # Fecha a conexão obrigatoriamente ao terminar

# Criar usuário e vincular a um perfil. 
@router.post("/", response_model=schemas.User)
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
@router.get("/", response_model=List[schemas.User])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Atualizar nome do usuário
@router.put("/{CPF}", response_model=schemas.User)
def atualizar_user(cpf: str, user_atualizado: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.cpf == cpf).first()
    
    '''if not db_user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Usuário não localizado")'''

    db_user.nome_user = user_atualizado.nome_user
    db.commit()
    db.refresh(db_user)
    return db_user

#Aplicar função de inativar usuário