# Importações
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# ----- PERFIL -----

class PerfilBase(BaseModel):
    nome_perfil: str # Ex: 'Paciente', 'Medico', 'Admin'

class PerfilCreate(PerfilBase):
    pass # Usado na criação de um novo perfil

class Perfil(PerfilBase):
    id_perfil: int
    model_config = ConfigDict(from_attributes=True) # Ler dados do SQLAlchemy

# ----- USUÁRIO -----

class UserBase(BaseModel):
    nome_user: str
    cpf: str
    id_perfil: int

class UserCreate(UserBase):
    senha_hash: str # Senha em texto puro que o usuário envia (será criptografada no banco)

class User(UserBase):
    id_user: int
    model_config = ConfigDict(from_attributes=True)
    # Não foi incluída a senha_hash aqui por segurança (LGPD)

class UserUpdate(BaseModel):
    nome_user: str
    model_config = ConfigDict(from_attributes=True)


# ----- PACIENTE -----

class PacienteBase(BaseModel):
    id_user: int
    data_nascimento: str
    tipo_sanguineo: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id_paciente: int
    user: User # Traz os dados básicos do usuário vinculado
    model_config = ConfigDict(from_attributes=True)

class PacienteUpdate(BaseModel):
    data_nascimento: str
    model_config = ConfigDict(from_attributes=True)

# ----- MÉDICO -----

class MedicoBase(BaseModel):
    id_user: int
    registro_profissional: str
    especialidade: str

class MedicoCreate(MedicoBase):
    id_user: int

class Medico(MedicoBase):
    id_medico: int
    user: User # Traz os dados básicos do usuário vinculado
    model_config = ConfigDict(from_attributes=True)

class MedicoUpdate(BaseModel):
    especialidade: str
    model_config = ConfigDict(from_attributes=True)

# ----- CONSULTA E PRONTUÁRIO -----

class ProntuarioBase(BaseModel):
    prescricao_digital: str
    descricao_clinica: str

class ProntuarioCreate(ProntuarioBase):
    id_consulta: int

class Prontuario(ProntuarioBase):
    id_prontuario: int
    data_atualizacao: datetime
    model_config = ConfigDict(from_attributes=True)

class ConsultaBase(BaseModel):
    id_paciente: int
    id_medico: int
    data_consulta: str
    hora_consulta: str
    tipo_consulta: str # "Presencial" ou "Telemedicina"
    status: str # "Agendada", "Realizada", etc.

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id_consulta: int
    data_consulta: str
    hora_consulta: str
    prontuario: Optional[Prontuario] = None # Opcional pois o prontuário só aparece se existir e o usuário tiver permissão
    model_config = ConfigDict(from_attributes=True)

# ----- LOGS (AUDITORIA) -----

class LogAuditoria(BaseModel):
    id_log: int
    id_user: int
    acao: str
    data_hora: datetime
    ip_origem: str
    model_config = ConfigDict(from_attributes=True)