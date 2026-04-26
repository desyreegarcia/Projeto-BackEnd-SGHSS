#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from ..models.database import get_db
from typing import List

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/user", tags=["Usuário"])

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
@router.put("/{id_user}", response_model=schemas.User)
def atualizar_user(id_user: int, user_atualizado: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id_user == id_user).first()
    
    '''if not db_user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Usuário não localizado")'''

    db_user.nome_user = user_atualizado.nome_user
    db.commit()
    db.refresh(db_user)
    return db_user

#Aplicar função de inativar usuário