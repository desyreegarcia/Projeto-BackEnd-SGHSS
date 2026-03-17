#Imports
from sqlalchemy import create_engine # Criar a conexão com o banco
from sqlalchemy.ext.declarative import declarative_base # Base para criar as tabelas
from sqlalchemy.orm import sessionmaker # Criador de sessões de banco de dados

# Define o endereço e nome do arquivo do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sghss.db"

# Comunicação com o SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Sessões para que cada requisição tenha sua própria conexão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que todas as tabelas irão herdar
Base = declarative_base()