#Importações e bibliotecas
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text # Tipos de colunas
from sqlalchemy.orm import relationship # Função para criar vínculos entre tabelas
from .database import Base # Base que foi criada no arquivo database.py
import datetime # Para manipular datas e horas

# Define a tabela de Administradores do sistema
class Admin(Base):
    __tablename__ = "admins" # Nome da tabela no banco de dados
    id_admin = Column(Integer, primary_key=True, index=True) # Chave primária
    nome = Column(String) # Nome do adm
    email = Column(String, unique=True) # E-mail - não pode repetir
    senha_hash = Column(String) # Senha criptografada
    perfil_acesso = Column(String) # Nível de permissão (Admin, Recepção, etc)

# Tabela de Pacientes
class Paciente(Base):
    __tablename__ = "pacientes" # Nome da tabela no banco
    id_paciente = Column(Integer, primary_key=True, index=True) # Id paciente
    cpf = Column(String, unique=True) # CPF do paciente - não pode repetir
    nome = Column(String) # Nome do paciente
    data_nascimento = Column(String) # Data de nascimento do paciente
    tipo_sanguineo = Column(String) # Informação importante do paciente
    
    # Ligação entre paciente e consultas, para consultar históricos
    consultas = relationship("Consulta", back_populates="paciente")

# Tabela de Médicos/Profissionais de Saúde
class Medico(Base):
    __tablename__ = "medicos" # Nome da tabela no banco
    id_medico = Column(Integer, primary_key=True, index=True) # Id médico
    registro_profissional = Column(String, unique=True) # CRM ou registro - não pode repetir
    nome = Column(String) # Nome do médico
    especialidade = Column(String) # Especialidade médica
    
    # Ligação entre médico e consultas, para gerenciar sua agenda
    consultas = relationship("Consulta", back_populates="medico")

# Tabela de Consultas
class Consulta(Base):
    __tablename__ = "consultas" # Nome da tabela no banco
    id_consulta = Column(Integer, primary_key=True, index=True) # ID da consulta
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente")) # Link com a tabela Paciente
    id_medico = Column(Integer, ForeignKey("medicos.id_medico")) # Link com a tabela Médico
    data_hora = Column(DateTime, default=datetime.datetime.utcnow) # Data/Hora da consulta
    tipo_consulta = Column(String) # Define se é "Presencial" ou "Telemedicina"
    status = Column(String) # Define se está "Agendada", "Cancelada" ou "Realizada"

    # Objetos relacionados
    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")