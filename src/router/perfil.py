#Imports
from fastapi import APIRouter, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from ..models.database import get_db
from typing import List

# Inicializa a aplicação FastAPI com título para o Swagger
router = APIRouter(prefix="/perfis", tags=["Perfil de Acesso"])

# Criar perfil de acesso
@router.post("/", response_model=schemas.Perfil)
def criar_perfil(perfil: schemas.PerfilCreate, db: Session = Depends(get_db)):
    db_perfil = models.Perfil(nome_perfil=perfil.nome_perfil)
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

# Listar perfis
@router.get("/", response_model=List[schemas.Perfil])
def listar_perfis(db: Session = Depends(get_db)): 
    return db.query(models.Perfil).all()

# Atualizar perfil buscando pelo id_perfil
@router.put("/{id_perfil}", response_model=schemas.Perfil)
def atualizar_perfil(id_perfil: int, perfil_atualizado: schemas.PerfilCreate, db: Session = Depends(get_db)):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.id_perfil == id_perfil).first()
    db_perfil.nome_perfil = perfil_atualizado.nome_perfil
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

# Deixei sem a função delete pois a intenção é ter perfis pré-definidos e usuários sempre linkados a estes perfis