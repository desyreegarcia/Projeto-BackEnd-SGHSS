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
    # Verifica se o CPF já existe para evitar duplicidade (Requisito de integridade)
    usuario_existente = db.query(models.User).filter(models.User.cpf == usuario.cpf).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    # Criar objeto no banco de dados
    db_user = models.User(
        nome_user=usuario.nome_user,
        cpf=usuario.cpf,
        senha_hash=usuario.senha, # Simulando o armazenamento do hash
        id_perfil=usuario.id_perfil
    )
    
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
    # Busca no banco se já existe alguém com o mesmo CPF
    db_paciente = db.query(models.Paciente).filter(models.Paciente.cpf == paciente.cpf).first()
    if db_paciente:
        # Se existir, retorna um erro para o usuário (Código 400)
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    # Converte os dados recebidos no formulário para o formato do banco de dados
    novo_paciente = models.Paciente(**paciente.model_dump())
    db.add(novo_paciente) # Adiciona o novo registro na "fila" do banco
    db.commit() # Grava permanentemente as alterações no db
    db.refresh(novo_paciente) # Atualiza o objeto com o ID gerado pelo banco
    return novo_paciente # Retorna o paciente cadastrado para confirmação

# Listar pacientes cadastrados
@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=["Pacientes"])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all() # Busca todos os registros e retorna

# ----- MÉDICOS -----

# Cadastrar um novo médico
@app.post("/medicos/", response_model=schemas.Medico, tags=["Médicos"])
def criar_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    # Verifica se o Registro Profissional já existe (Segurança de Dados)
    db_medico = db.query(models.Medico).filter(models.Medico.registro_profissional == medico.registro_profissional).first()
    if db_medico:
        # Retorna erro se o médico já estiver no sistema
        raise HTTPException(status_code=400, detail="Médico já cadastrado com este registro")
    
    # Transforma os dados recebidos para o formato do banco de dados
    novo_medico = models.Medico(**medico.model_dump())
    db.add(novo_medico) # Prepara a inserção
    db.commit() # Salva no db
    db.refresh(novo_medico) # Atualiza com o ID gerado
    return novo_medico # Retorna os dados do médico cadastrado

# Listar todos os médicos
@app.get("/medicos/", response_model=list[schemas.Medico], tags=["Médicos"])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(models.Medico).all() # Busca e retorna todos os médicos'''