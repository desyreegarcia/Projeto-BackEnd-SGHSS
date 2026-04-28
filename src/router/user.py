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
    # Verifica se o CPF já existe / Se existir, retorna erro
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

# Atualizar nome do usuário buscando pelo id_user.
# Deixei apenas a atualização do nome, pois os outros campos (CPF e perfil) não devem ser alterados com facilidade.
@router.put("/{id_user}", response_model=schemas.User)
def atualizar_user(id_user: int, user_atualizado: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id_user == id_user).first()
    db_user.nome_user = user_atualizado.nome_user
    db.commit()
    db.refresh(db_user)
    return db_user

# Deixei sem a função delete pois a intenção é ter usuários sempre vinculados a um perfil e a consultas, e não excluir estes dados do sistema.