# FATO MOV ORÇAMENTO

Este projeto é um script Python desenvolvido para automatizar a extração, processamento e envio de dados relacionados a orçamentos e diferenças financeiras. Ele se conecta a bancos de dados SQL Server, executa consultas específicas, processa os resultados e envia relatórios por e-mail.

## Funcionalidades

1. **Conexão com Bancos de Dados**:
   - O script se conecta a dois bancos de dados SQL Server:
     - `HubDados`: Para extrair dados orçados.
     - `FINANCA`: Para extrair diferenças financeiras.

2. **Execução de Consultas SQL**:
   - As consultas SQL são armazenadas no módulo `query` e executadas utilizando a biblioteca `SQLAlchemy`.

3. **Processamento de Dados**:
   - Os resultados das consultas são carregados em DataFrames do Pandas para processamento.

4. **Armazenamento de Dados**:
   - Os dados extraídos são inseridos em um novo banco de dados utilizando a função `insert_df_new_engine`.

5. **Envio de Relatórios por E-mail**:
   - Caso sejam encontradas diferenças financeiras, o script gera um relatório em formato HTML e o envia por e-mail utilizando a função `enviar_email`.

6. **Tratamento de Erros**:
   - O script possui tratamento de exceções para capturar e exibir erros durante a execução.

## Estrutura do Projeto

- **`main.py`**: Arquivo principal que contém a lógica de execução do script.
- **`db_config.py`**: Contém funções auxiliares para criar conexões com o banco de dados e manipular DataFrames.
- **`query.py`**: Armazena as consultas SQL utilizadas no script.
- **`email_sender.py`**: Implementa a funcionalidade de envio de e-mails.

## Requisitos

- Python 3.8 ou superior.
- Dependências listadas no arquivo `requirements.txt`:
  - `pandas`
  - `sqlalchemy`
  - `pyodbc`
  - `tabulate`

## Configuração

1. **Instalação de Dependências**:
   Execute o comando abaixo para instalar as dependências necessárias:
   ```bash
   pip install -r requirements.txt