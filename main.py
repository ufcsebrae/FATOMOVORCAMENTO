from db_config import close_connection,insert_df_new_engine
from query import queries
from sqlalchemy import create_engine,text
from datetime import datetime
from tabulate import tabulate
from email_sender import enviar_relatorio_email
import pandas as pd


def main():
      
      servername = "spsvsql39\\metas"
      dbname = "HubDados"
      engine = create_engine(
        f'mssql+pyodbc://@{servername}/{dbname}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    )
      try:
            with engine.connect() as connection:
                  # 🔍 Carrega os resultados diretamente em um DataFrame
                  df = pd.read_sql_query(sql=text(queries["orcado"]),con=connection)
                  
                  insert_df_new_engine(df, "orcado")
              
      except Exception as e: #❌ printa erro
            print(f"Erro durante a execução orcado: {e}")

      finally:
                  close_connection(engine)
      
      servername2 = "spsvsql39\\metas"
      dbname2 = "FINANCA"
      engine2 = create_engine(
             f'mssql+pyodbc://@{servername2}/{dbname2}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    )
      try:
            with engine2.connect() as connection2:
                  # 🔍 Carrega os resultados diretamente em um DataFrame
                  df2 = pd.read_sql_query(sql=text(queries["diferencas"]),con=connection2)
                  destinatario = "orcamento@sp.sebrae.com.br"
                  assunto = f"Diferenças Orçamento - {datetime.now().strftime('%d/%m/%Y')}"
                  corpo = df2.to_html(index=False, justify="center", border=1, classes="table table-striped table-bordered")
                  if not df2.empty:
                        enviar_relatorio_email(destinatario, assunto, df2)
                        print(tabulate(df2, headers="keys",tablefmt="fancy_grid"))
                  if df2.empty:
                        print(f"DataFrame de diferenças vazio")

      except Exception as e: #❌ printa erro
            print(f"Erro durante a execução diferencas: {e}")

      finally:
                  close_connection(engine2)

if __name__ == "__main__": 
    main()
  