import win32com.client as win32
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def enviar_relatorio_email(destinatario, ASSUNTO, dataframe):
    data_hoje = datetime.today().strftime("%d/%m/%Y")
    TEXTO_CORPO = f"""
    <p>Prezados,</p>
    <p>Segue tabela com a diferença de orçamento atualizada no dia <strong>{data_hoje}</strong>.</strong></p>"""
    
    # Formatando os valores para moeda brasileira
    dataframe["VALOR_DIA_ATUAL"] = dataframe["VALOR_DIA_ATUAL"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    dataframe["VALOR_DIA_ANTERIOR"] = dataframe["VALOR_DIA_ANTERIOR"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    dataframe["DIFERENCA"] = dataframe["DIFERENCA"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    env = Environment(loader=FileSystemLoader("C:/Users/e_gabrielapr/teste/Movimento Orçamento/FATOMOVORCAMENTO"))
    try:
        template = env.get_template("email_template.html")
    except Exception as e:
        print(f"❌ Erro ao carregar o template: {e}")
        return
    
    CORPO = template.render(
        assunto=ASSUNTO,    
        tabelas=dataframe.to_html(index=False, justify="center", border=1, classes="table table-striped table-bordered"),
        texto_email=TEXTO_CORPO
    )

    try:
        outlook = win32.Dispatch("Outlook.Application")
        mensagem = outlook.CreateItem(0)
        mensagem.Subject = ASSUNTO
        mensagem.HTMLBody = CORPO
        mensagem.To = destinatario

        mensagem.Send()
        print("📧 E-mail enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar o e-mail: {e}")
