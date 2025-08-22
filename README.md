# API Censo Escolar 🏫

API para consulta e gestão de dados do Censo Escolar, desenvolvida em Flask.

## 📋 Pré-requisitos

- Python 3.8+
- Git
- Pip

## 🚀 Como Iniciar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/censo-escolar-api.git
cd censo-escolar-api
```

### 2. instalção do ambiente virtual
```bash
python -m venv venv
```

## 3. Ativação do ambiente
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 4. Instalar dependências
```bash
pip install -r requirements.txt
```

## 5. Iniciar a API
```bash
flask run
# ou
python app.py
```

## 6. Adição do SQLite como banco simples

Para testar, execute o arquivo init_db.py, que será o inicializador do nosso banco, ele será responsavél por pegar o nosso schema.sql e montar nossa tabela instituicoes

Após isso, execute o migrate_sql.py que será responsável por migrar nossos dados presentes no arquivo censo_escolar.json para o banco sql

Finalizando, execute o "flask run" e faça as requisições para testar


## 7. Comandos para executar

python -m venv venv 
pip install -r requirements.txt 