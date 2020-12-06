import smtplib, ssl

def enviar_correo(receiver_email, asunto, m):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "gerentebbgm@gmail.com"
    password = "Miniproyecto2020"
    message = """\
Subject: {0}
{1} """.format(asunto,m)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
