# Projeto-BackEnd-SGHSS
Projeto de desenvolvimento BackEnd - Sistema de Gestão Hospitalar e de Serviços de Saúde

Sobre o Projeto
Este projeto foi desenvolvido como parte do Projeto Multidisciplinar do curso de Análise e Desenvolvimento de Sistemas da Uninter. O objetivo é centralizar a gestão de atendimentos, profissionais de saúde e pacientes da instituição VidaPlus.O foco desta implementação é o Back-end, priorizando a segurança dos dados (LGPD), escalabilidade e o suporte à telemedicina

Tecnologias:
Linguagem: Python
Framework: FastAPI
Banco de Dados: SQLite seguindo o modelo DER
Documentação de API: Swagger/OpenAPI.

Funcionalidades:
Gestão de Pacientes: Cadastro completo e histórico clínico.
Gestão Médica: Agendas de profissionais e emissão de receitas digitais.
Agendamento: Sistema de marcação de consultas presenciais e telemedicina.
Segurança: Controle de acesso por perfil (Admin, Médico, Paciente) e logs de auditoria.

Estrutura de Pastas
├── docs/               # Diagramas (Casos de Uso, Classes, DER)
├── src/
│   ├── models/         # Definição das tabelas do banco
│   ├── routes/         # Endpoints da API
│   ├── services/       # Regras de negócio
│   └── main.py         # Arquivo de inicialização
├── requirements.txt    # Dependências do projeto
└── README.md

Como Executar o Projeto
Clone o repositório:
Bash
git clone [LINK_DO_SEU_REPOSITORIO]
Instale as dependências:
Bash
pip install -r requirements.txt
Inicie o servidor:
Bash
python main.py


Nome: Desyree Garcia.
RU: 986134.
