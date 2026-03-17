from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Admin(Base):
    __tablename__ = "admins"
    id_admin = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)
    perfil_acesso = Column(String)

class Paciente(Base):
    __tablename__ = "pacientes"
    id_paciente = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True)
    nome = Column(String)
    data_nascimento = Column(String)
    tipo_sanguineo = Column(String)
    
    consultas = relationship("Consulta", back_populates="paciente")

class Medico(Base):
    __tablename__ = "medicos"
    id_medico = Column(Integer, primary_key=True, index=True)
    registro_profissional = Column(String, unique=True)
    nome = Column(String)
    especialidade = Column(String)
    
    consultas = relationship("Consulta", back_populates="medico")

class Consulta(Base):
    __tablename__ = "consultas"
    id_consulta = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"))
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"))
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    tipo_consulta = Column(String)
    status = Column(String)

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")