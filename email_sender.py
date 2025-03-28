import win32com.client as win32
def enviar_email(destinatario, assunto, corpo):
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)  
    mail.To = destinatario
    mail.Subject = assunto
    mail.HTMLBody = corpo 
    mail.Send()
    print("E-mail enviado com sucesso!")