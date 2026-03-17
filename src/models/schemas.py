from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Formulário para criar um Paciente
class PacienteCreate(BaseModel):
    cpf: str
    nome: str
    data_nascimento: str
    tipo_sanguineo: str

# Como o Paciente aparecerá na resposta (com o ID)
class Paciente(PacienteCreate):
    id_paciente: int
    class Config:
        from_attributes = True

# Formulário para criar um Médico
class MedicoCreate(BaseModel):
    registro_profissional: str
    nome: str
    especialidade: str

class Medico(MedicoCreate):
    id_medico: int
    class Config:
        from_attributes = True