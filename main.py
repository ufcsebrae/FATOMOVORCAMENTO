from db_config import close_connection,insert_df_new_engine
from query import queries
from sqlalchemy import create_engine,text
from datetime import datetime
from tabulate import tabulate
from email_sender import enviar_relatorio_email
import pandas as pd 


def main():
       #conexão com o banco de dados e execução da query que preenche o FINANCA
      servername = "spsvsql39"
      dbname = "HubDados"
      engine = create_engine(
        f'mssql+pyodbc://@{servername}/{dbname}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    )
      try:
            with engine.connect() as connection:
                  hoje = datetime.now().strftime('%Y-%m-%d')
                  print(f"Data de hoje: {hoje}")

                  # Consulta para obter a data máxima de atualização
                  query_max_data = "SELECT MAX(data_atualizacao) FROM financa.dbo.orcado"
                  max_data = pd.read_sql_query(sql=text(query_max_data), con=connection).iloc[0, 0]

                   # Verifica se a data máxima é igual à data de hoje
                  if str(max_data) == hoje:
                        print("Encontrado dados de hoje, deletando...")
                        # Query para deletar registros com a data de hoje     
                        connection.execute(
                              text("DELETE FROM financa.dbo.orcado WHERE data_atualizacao = :hoje"),
                              {"hoje": hoje}
                        )
                        connection.commit()
                        print("Remoção concluída com sucesso")
                       
                  print("Printando dados de hoje")      
                  df = pd.read_sql_query(sql=text(queries["orcado"]),con=connection)
                  
                  insert_df_new_engine(df, "orcado")
              
      except Exception as e: #❌ printa erro
            print(f"Erro durante a execução orcado: {e}")

      finally:
                  close_connection(engine)
      
      servername2 = "spsvsql39"
      dbname2 = "FINANCA"
      engine2 = create_engine(
             f'mssql+pyodbc://@{servername2}/{dbname2}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    )
      try:
            with engine2.connect() as connection2:
                  # 🔍 Carrega os resultados diretamente em DataFrames
                  df2 = pd.read_sql_query(sql=text(queries["diferencas"]),con=connection2)
                  df3 = pd.read_sql_query(sql=text(queries["CC"]),con=connection2)
                  df4 = pd.read_sql_query(sql=text(queries["ID"]),con=connection2)
                  destinatario = "orcamento@sp.sebrae.com.br"
                  assunto = f"Diferenças Orçamento - {datetime.now().strftime('%d/%m/%Y')}"
                  
                  if not df2.empty:
                        enviar_relatorio_email(destinatario, assunto, df2,df3,df4)
                        print(f"Essa é a tabela DIFERENCAS:\n\n{tabulate(df2, headers='keys',tablefmt='grid',numalign='left', stralign='left')}")
                        print(f"Essa é a tabela CC:\n\n{tabulate(df3, headers='keys', tablefmt='grid', numalign='left', stralign='left')}")
                        print(f"Essa é a tabela ID:\n\n{tabulate(df4, headers='keys',tablefmt='grid',numalign='left', stralign='left')}")
                  if df2.empty:
                        print(f"DataFrame de diferenças vazio")
                  if df3.empty:
                        print(f"DataFrame de cc vazio")
                  if df4.empty:
                        print(f"DataFrame de id vazio")

      except Exception as e: #❌ printa erro
            print(f"Erro durante a execução: {e}")

      finally:
                  close_connection(engine2)

if __name__ == "__main__": 
    main()
  
