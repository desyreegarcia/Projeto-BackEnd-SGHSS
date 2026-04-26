#Imports
from fastapi import APIRouter, FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from ..models import models, schemas, database # Arquivos internos
from ..models.database import get_db
from typing import List

# Inicializa a aplicação FastAPI com título e versão para o Swagger
router = APIRouter(prefix="/consultas", tags=["Consultas"])

# --- ROTAS PARA CONSULTAS/ATENDIMENTOS ---

# Criar consulta
@router.post("/", response_model=schemas.Consulta)
def agendar_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):

    # Busca o paciente no banco de dados usando o ID / Se não for encontrado, retorna erro 404
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id_paciente == consulta.id_paciente).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado no sistema.")

    # Busca o médico no banco de dados usando o ID / Se não for encontrado, retorna erro 404
    db_medico = db.query(models.Medico).filter(models.Medico.id_medico == consulta.id_medico).first()
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado no sistema.")

    # Cria a Consulta
    db_consulta = models.Consulta(**consulta.model_dump())
    db_consulta.status = "Agendada"
    
    # Adiciona ao db
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Cancelar uma consulta - Utiliza o método PUT pois trata-se de um dado existente
@router.put("/{id_consulta}/cancelar", response_model=schemas.Consulta)
def cancelar_consulta(id_consulta: int, db: Session = Depends(get_db)):
    # Busca a consulta no banco de dados / Se não for encontrada, retorna erro 404 
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id_consulta == id_consulta).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    
    # Atualiza o campo status automaticamente para 'Cancelada'
    db_consulta.status = "Cancelada"
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Listar as consultas de um paciente específico
@router.get("/paciente/{id_paciente}", response_model=List[schemas.Consulta])
def listar_historico_paciente(id_paciente: int, db: Session = Depends(get_db)):
    consultas = db.query(models.Consulta).filter(models.Consulta.id_paciente == id_paciente).all()
    return consultas

# Médico visualizar sua agenda/lista de atendimentos
@router.get("/medico/{id_medico}", response_model=List[schemas.Consulta])
def listar_agenda_medico(id_medico: int, db: Session = Depends(get_db)):
    agenda = db.query(models.Consulta).filter(models.Consulta.id_medico == id_medico).all()