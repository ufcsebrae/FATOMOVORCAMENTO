# db_config.py
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError

# Definir as variáveis da conexão
servername = "spsvsql39\\metas"
dbname = "FINANCA"
driver = "ODBC+Driver+17+for+SQL+Server"

# String de conexão
connection_string = (
    f"mssql+pyodbc://@{servername}/{dbname}?"
    f"trusted_connection=yes&driver={driver}"
)

def create_engine_():
    """Cria e retorna a engine do banco de dados."""
    return create_engine(connection_string)

def close_connection(engine):
    """Encerra a conexão com o banco de dados."""
    if engine:
        engine.dispose()
        print("Conexão encerrada com sucesso.")

def insert_df_new_engine(df: pd.DataFrame, nome_tabela: str):
    """
    Insere um DataFrame em uma tabela no SQL Server.
    Se a tabela já existir, ela será removida e recriada.
    """
    df['data_atualizacao'] = pd.to_datetime("today").date()
    
    engine = create_engine_()  # Obtém a engine de conexão
    conn = engine.connect()
    print(df)
    try:
        with engine.connect() as conn:
            
            # Insere os dados recriando a tabela
            df.to_sql(
                nome_tabela,
                con=engine,
                schema="dbo",
                if_exists='append', # Se a tabela já existir, insere os dados
                index=False,
                method='multi',  # Otimiza inserção em lote
                chunksize=75
            )

            print(f"✅ Tabela '{nome_tabela}' recriada e dados inseridos.")

    except SQLAlchemyError as e:
        print(f"❌ Erro ao inserir dados: {e}")

    finally:
        close_connection(engine)  # Fecha a conexão corretamente
