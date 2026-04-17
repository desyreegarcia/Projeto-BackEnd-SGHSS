#Importações e bibliotecas
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text # Tipos de colunas
from sqlalchemy.orm import relationship # Função para criar vínculos entre tabelas
from .database import Base # Base que foi criada no arquivo database.py
import datetime # Para manipular datas e horas

# Tabela de Perfil de acesso
class Perfil(Base):
    __tablename__ = "perfil" # Nome da tabela no banco de dados
    id_perfil = Column(Integer, primary_key=True, index=True)
    nome_perfil = Column(String) #(1 = 'Admin', 2 = 'Paciente', 3 = 'Medico', )

# --- Tabela de Usuarios ---
class User(Base):
    __tablename__ = "user"
    id_user = Column(Integer, primary_key=True, index=True)
    id_perfil = Column(Integer, ForeignKey("perfil.id_perfil")) # Link com a tabela Perfil
    nome_user = Column(String)
    cpf = Column(String, unique=True) # CPF - não pode repetir
    senha_hash = Column(String) # Senha criptografada
    user_ativo = Column(Boolean, default=True)

    perfil = relationship("Perfil") # Um usuário tem um perfil


# --- Tabela de Pacientes ---
class Paciente(Base):
    __tablename__ = "pacientes"
    id_paciente = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id_user")) # Link com a tabela Perfil
    data_nascimento = Column(String)
    tipo_sanguineo = Column(String)
    
    user = relationship("User") # Um paciente é um usuário específico

# --- Tabela de Médicos/Profissionais de Saúde ---
class Medico(Base):
    __tablename__ = "medicos"
    id_medico = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id_user")) # Link com a tabela Perfil
    registro_profissional = Column(String, unique=True) # CRM - não pode repetir
    especialidade = Column(String)
    
    user = relationship("User") # Um médico é um usuário específico

# --- Tabela de Consultas ---
class Consulta(Base):
    __tablename__ = "consulta"
    id_consulta = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente")) # Link com a tabela Paciente
    id_medico = Column(Integer, ForeignKey("medicos.id_medico")) # Link com a tabela Médico
    data_consulta = Column(String)
    hora_consulta = Column(String)
    tipo_consulta = Column(String) # Presencial ou Telemedicina
    status = Column(String) # "Agendada", "Cancelada" ou "Realizada"

    # Objetos relacionados
    paciente = relationship("Paciente")
    medico = relationship("Medico")
    prontuario = relationship("Prontuarios", back_populates="consulta", uselist=False) # uselist=False pois é 1 para 1

# --- Tabela de Prontuario ---
class Prontuarios(Base):
    __tablename__ = "prontuario"
    id_prontuario = Column(Integer, primary_key=True, index=True)
    id_consulta = Column(Integer, ForeignKey("consulta.id_consulta")) # Link com a tabela Paciente
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow) # Data/Hora da consulta
    prescricao_digital = Column(String)
    descricao_clinica = Column(String)

    consulta = relationship("Consulta", back_populates="prontuario")

# --- Tabela de Auditoria (Conformidade com LGPD) ---
class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"
    id_log = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id_user")) # Quem acessou
    acao = Column(String) # Ex: "Acesso ao Prontuário ID 50"
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    ip_origem = Column(String) # Registro de onde partiu a requisição

    # Objeto relacionado: permite acessar log.user.nome_user diretamente
    user = relationship("User")