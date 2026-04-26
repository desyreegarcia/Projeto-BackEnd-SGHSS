# Importações
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# ----- PERFIL -----

class PerfilBase(BaseModel):
    nome_perfil: str # Ex: 'Paciente', 'Medico', 'Admin'

class PerfilCreate(PerfilBase):
    pass # Usado na criação de um novo perfil

class Perfil(PerfilBase, BaseSchema):
    id_perfil: int

# ----- USUÁRIO -----

class UserBase(BaseModel):
    nome_user: str
    cpf: str
    id_perfil: int

class UserCreate(UserBase):
    senha_hash: str # Senha em texto puro que o usuário envia (será criptografada no banco)

class User(UserBase, BaseSchema):
    id_user: int
    # Não foi incluída a senha_hash aqui por segurança (LGPD)

class UserUpdate(BaseSchema):
    nome_user: str

# ----- PACIENTE -----

class PacienteBase(BaseModel):
    id_user: int
    data_nascimento: str
    tipo_sanguineo: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase, BaseSchema):
    id_paciente: int
    user: User # Traz os dados básicos do usuário vinculado

class PacienteUpdate(BaseSchema):
    data_nascimento: str

# ----- MÉDICO -----

class MedicoBase(BaseModel):
    id_user: int
    registro_profissional: str
    especialidade: str

class MedicoCreate(MedicoBase):
    id_user: int

class Medico(MedicoBase, BaseSchema):
    id_medico: int
    user: User # Traz os dados básicos do usuário vinculado

class MedicoUpdate(BaseSchema):
    especialidade: str

# ----- CONSULTA E PRONTUÁRIO -----

class ProntuarioBase(BaseModel):
    prescricao_digital: str
    descricao_clinica: str

class ProntuarioCreate(ProntuarioBase):
    id_consulta: int

class Prontuario(ProntuarioBase, BaseSchema):
    id_prontuario: int
    data_atualizacao: datetime

class ConsultaBase(BaseModel):
    id_paciente: int
    id_medico: int
    data_consulta: str
    hora_consulta: str
    tipo_consulta: str # "Presencial" ou "Telemedicina"
    status: str # "Agendada", "Realizada", etc.

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase, BaseSchema):
    id_consulta: int
    data_consulta: str
    hora_consulta: str
    prontuario: Optional[Prontuario] = None # Opcional pois o prontuário só aparece se existir e o usuário tiver permissão

# ----- LOGS (AUDITORIA) -----

class LogAuditoria(BaseSchema):
    id_log: int
    id_user: int
    acao: str
    data_hora: datetime
    ip_origem: str