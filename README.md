# Projeto de desenvolvimento BackEnd - Sistema de Gestão Hospitalar e de Serviços de Saúde

### Sobre o Projeto:
Este projeto foi desenvolvido como parte do Projeto Multidisciplinar do curso de Análise e Desenvolvimento de Sistemas da Uninter. O objetivo é centralizar a gestão de atendimentos, profissionais de saúde e pacientes da instituição VidaPlus.O foco desta implementação é o Back-end, priorizando a segurança dos dados (LGPD), escalabilidade e o suporte à telemedicina

### Funcionalidades:
O **SGHSS** é uma API back-end desenvolvida com **FastAPI** e **SQLAlchemy**. O projeto foi estruturado por modularização, separando rotas, modelos de banco de dados e esquemas de validação para garantir um sistema escalável, seguro e de fácil manutenção.
* Gestão de Pacientes: Cadastro completo e histórico clínico.
* Gestão Médica: Agendas de profissionais e emissão de receitas digitais.
* Agendamento: Sistema de marcação de consultas presenciais e telemedicina.
* Segurança: Controle de acesso por perfil (Admin, Médico, Paciente) e logs de auditoria.

### Tecnologias

* **Python 3.11+**: Linguagem base do projeto.
* **FastAPI**: Framework moderno de alta performance para construção de APIs.
* **SQLAlchemy**: ORM (Object Relational Mapper) para manipulação simplificada do banco de dados.
* **SQLite**: Banco de dados relacional leve para armazenamento local.
* **Pydantic v2**: Validação rigorosa de dados e tipagem de contratos (Schemas).
* **Docker**: Containerização para facilitar o deploy e padronização do ambiente.

### Estrutura do Projeto

O projeto adota uma arquitetura organizada por responsabilidades, facilitando a navegação no código:

```text
src/
├── main.py              # Ponto de entrada e registro de rotas (FastAPI)
├── models/
│   ├── database.py      # Conexão, sessão e função get_db
│   ├── models.py        # Definição das tabelas e relacionamentos (SQLAlchemy)
│   └── schemas.py       # Validação e contratos de dados (Pydantic)
└── router/
    ├── perfil.py        # CRUD de Perfis de Acesso
    ├── user.py          # Gestão de Usuários (RBAC)
    ├── paciente.py      # Dados específicos de Pacientes
    ├── medicos.py       # Gestão de Profissionais de Saúde
    └── atendimentos.py  # Agendamentos, Consultas e Prontuários
```

### Como Executar o Projeto

1 - Clone o repositório:
```Bash
git clone https://github.com/desyreegarcia/Projeto-BackEnd-SGHSS
cd Projeto-BackEnd-SGHSS
```

2 - Execução via Docker (Recomendado)

```Bash
# Construir a imagem
docker build -t sghss-backend .
# Rodar o container
docker run -d -p 8000:8000 sghss-backend
```

3 - Execução local

```Bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
python -m uvicorn src.main:app --reload
```

## Acesse a Documentação Interativa:
Após iniciar o servidor, acesse **http://127.0.0.1:8000/docs** para testar os endpoints via Swagger UI.

---

### Nome: Desyree Garcia.
### RU: 986134.