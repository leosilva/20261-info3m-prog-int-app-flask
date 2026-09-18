# Projeto INFO3M

Aplicação web desenvolvida em Python com Flask, SQLAlchemy, SQLite e MySQL.

## Tecnologias

- Python;
- Flask;
- Flask-WTF e WTForms;
- Flask-SQLAlchemy;
- SQLAlchemy;
- MySQL;
- Bootstrap/SB Admin 2, CSS e JavaScript.

## Pré-requisitos

- Python 3.12 ou superior;
- MySQL Server em execução;
- banco de dados `2026-info3m` criado no MySQL;
- usuário do MySQL com permissão para acessar esse banco.

## Instalação

Clone o projeto e entre na pasta:

```bash
git clone <url-do-repositorio>
cd app_flask
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate       # Windows
```

Instale as dependências declaradas e os drivers usados pela aplicação:

```bash
pip install -r requirements.txt
```

## Configuração do banco

Crie o banco de dados:

```sql
CREATE DATABASE `2026-info3m`;
```

Por padrão, a aplicação usa:

| Variável | Padrão | Descrição |
|---|---|---|
| `DB_USERNAME` | `root` | Usuário do MySQL |
| `DB_PASSWORD` | `labinfo` | Senha do MySQL |

Para usar outros dados de acesso, exporte as variáveis antes de iniciar a aplicação:

```bash
export DB_USERNAME=seu_usuario
export DB_PASSWORD=sua_senha
```

O nome do banco, host e porta estão definidos em `config.py` como `2026-info3m`, `localhost` e `3306`. Na primeira inicialização, as tabelas são criadas automaticamente pelo SQLAlchemy.

## Executando o projeto

Com o ambiente virtual ativado, execute:

```bash
flask run --debug
```

Acesse no navegador: `http://127.0.0.1:5000/`.

## Estrutura do projeto

```text
app_flask/
├── app/
│   ├── forms/       # Formulários WTForms
│   ├── models/      # Modelos do banco de dados
│   ├── services/    # Regras de negócio e acesso aos dados
│   ├── static/      # CSS, JavaScript, imagens e fontes
│   ├── templates/   # Templates Jinja2
│   └── routes.py    # Rotas da aplicação
├── config.py        # Configurações do banco e da aplicação
├── requirements.txt # Dependências Python
└── run.py           # Ponto de entrada da aplicação
```

## Observações

- Não versione credenciais reais nem o arquivo `.env`.
- Altere `SECRET_KEY` em `config.py` antes de utilizar a aplicação em produção.
- O serviço de autenticação atual é apenas uma implementação inicial: o método de login sempre retorna sucesso e ainda não valida a senha no banco.
- O servidor de desenvolvimento do Flask é adequado para desenvolvimento local, não para produção.

## Solução de Problemas

- **Erro de conexão com o MySQL**: confirme se o serviço e o banco `2026-info3m` estão disponíveis, e se `DB_NAME`, `DB_USERNAME` e `DB_PASSWORD` estão corretos.
- **Porta 5000 ocupada**: encerre o processo que a utiliza antes de iniciar a aplicação.

## Licença

Este projeto inclui recursos visuais baseados no template [Start Bootstrap SB Admin 2](https://startbootstrap.com/theme/sb-admin-2), cuja licença está disponível em `startbootstrap-sb-admin-2-gh-pages/LICENSE`.
