#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from typing import List

# Comando que lê os modelos e cria as tabelas no arquivo sghss.db se elas não existirem
models.Base.metadata.create_all(bind=database.engine)

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/perfis", tags=["Perfil de Acesso"])

# Função de conexão com o banco
def get_db():
    db = database.SessionLocal() # Abre a conexão
    try:
        yield db # Entrega a conexão para a rota solicitada
    finally:
        db.close() # Fecha a conexão obrigatoriamente ao terminar

# ----- ROTAS PARA PERFIL -----

# Criar perfil de acesso
@router.post("/perfis/", response_model=schemas.Perfil)
def criar_perfil(perfil: schemas.PerfilCreate, db: Session = Depends(get_db)):
    db_perfil = models.Perfil(nome_perfil=perfil.nome_perfil)
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

# Listar perfis
@router.get("/perfis/", response_model=List[schemas.Perfil])
def listar_perfis(db: Session = Depends(get_db)): 
    return db.query(models.Perfil).all()

# Atualizar perfil
@router.put("/perfis/{id_perfil}", response_model=schemas.Perfil)
def atualizar_perfil(id_perfil: int, perfil_atualizado: schemas.PerfilCreate, db: Session = Depends(get_db)):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.id_perfil == id_perfil).first()
    
    if not db_perfil:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    db_perfil.nome_perfil = perfil_atualizado.nome_perfil
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

# Deletar perfil
@router.delete("/perfis/{id_perfil}")
def deletar_perfil(id_perfil: int, db: Session = Depends(get_db)):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.id_perfil == id_perfil).first()

    if not db_perfil:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    db.delete(db_perfil)
    db.commit()
    return {"detail": "Perfil removido com sucesso"}