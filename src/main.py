#Imports
from fastapi import FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo de dado para a sessão do banco
from .models import models, schemas, database # Arquivos internos
from typing import List

# Comando que lê os modelos e cria as tabelas no arquivo sghss.db se elas não existirem
models.Base.metadata.create_all(bind=database.engine)

# Inicializa a aplicação FastAPI com título e versão para o Swagger
app = FastAPI(title="SGHSS")

# Função de conexão com o banco
def get_db():
    db = database.SessionLocal() # Abre a conexão
    try:
        yield db # Entrega a conexão para a rota solicitada
    finally:
        db.close() # Fecha a conexão obrigatoriamente ao terminar

# ----- ROTAS PARA PERFIL -----

# Criar perfil de acesso
@app.post("/perfis/", response_model=schemas.Perfil, tags=["Perfil de Acesso"])
def criar_perfil(perfil: schemas.PerfilCreate, db: Session = Depends(get_db)):
    db_perfil = models.Perfil(nome_perfil=perfil.nome_perfil)
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

# Listar perfis
@app.get("/perfis/", response_model=List[schemas.Perfil], tags=["Perfil de Acesso"])
def listar_perfis(db: Session = Depends(get_db)): 
    return db.query(models.Perfil).all()

# ----- ROTAS PARA USUÁRIOS -----

# Criar usuário e vincular a um perfil. 
@app.post("/usuarios/", response_model=schemas.User, tags=["Usuários"])
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
@app.get("/usuarios/", response_model=List[schemas.User], tags=["Usuários"])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# ----- ROTA PARA PACIENTES -----

# Cadastrar um novo paciente
@app.post("/pacientes/", response_model=schemas.Paciente, tags=["Pacientes"])
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    
    # Adiciona ao db
    novo_paciente = models.Paciente(**paciente.model_dump())
    db.add(novo_paciente) # Adiciona
    db.commit() # Grava
    db.refresh(novo_paciente) # Atualiza
    return novo_paciente # Retorna

# Listar pacientes cadastrados
@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=["Pacientes"])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all() # Busca todos os registros e retorna

# ----- MÉDICOS -----

# Cadastrar um novo médico
@app.post("/medicos/", response_model=schemas.Medico, tags=["Médicos"])
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
@app.get("/medicos/", response_model=list[schemas.Medico], tags=["Médicos"])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(models.Medico).all()

# --- ROTAS PARA CONSULTAS/ATENDIMENTOS ---

# Criar consulta
@app.post("/consultas/", response_model=schemas.Consulta, tags=["Consultas"])
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
@app.put("/consultas/{id_consulta}/cancelar", response_model=schemas.Consulta, tags=["Consultas"])
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
@app.get("/consultas/paciente/{id_paciente}", response_model=List[schemas.Consulta], tags=["Consultas"])
def listar_historico_paciente(id_paciente: int, db: Session = Depends(get_db)):
    consultas = db.query(models.Consulta).filter(models.Consulta.id_paciente == id_paciente).all()
    return consultas

# Médico visualizar sua agenda/lista de atendimentos
@app.get("/consultas/medico/{id_medico}", response_model=List[schemas.Consulta], tags=["Consultas"])
def listar_agenda_medico(id_medico: int, db: Session = Depends(get_db)):
    agenda = db.query(models.Consulta).filter(models.Consulta.id_medico == id_medico).all()
    return agenda