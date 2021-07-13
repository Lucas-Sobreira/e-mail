import os
from flask import Flask, render_template, request, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import time

app = Flask(__name__, template_folder='public')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

cors = CORS(app, resource={r"/*": {"origins": "*"}})


@app.route('/')
def verificacao():
    return render_template('verificacao.html')


@app.route('/email', methods=['GET', 'POST'])
def verificacao_usuario():
    if request.method == 'POST':
        if request.form['nome'] == 'user' and request.form['senha'] == 'user':
            return render_template('email.html')
            # return redirect(url_for('upload'), code=302)  # Redirecionamento utiliza cod=302
        else:
            return 'Você digitou o login errado!'  # Na versão final retirar essa msg de erro
    return abort(403)


@app.route('/enviando', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        usuarios = []
        endereco_email = []

        file = request.files['file']
        savepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(savepath)

        time.sleep(2)

        df_emails = pd.read_csv('upload/emails.txt', delimiter=';')  #MUDAR PARA A EXTENSÂO DO ARQUIVO
        for i in range(len(df_emails)):
            usuarios.append((df_emails['usuario'][i]).title())
            endereco_email.append(df_emails['email'][i])

        # Setando o pacote SMTP
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.starttls()
        my_address = request.form['login']
        password = request.form['senha']
        s.login(my_address, password)

        for i in range(len(usuarios)):
            # create a message
            msg = MIMEMultipart()

            # setup the parameters of the message/ Colocando os parametros para a mensagem
            msg['From'] = my_address
            msg['To'] = endereco_email[i]
            msg['Subject'] = "E-mail Marketing"

            # add in the actual person name to the message template
            carimbo = """
                        <p><br></p>
                        <p>&nbsp;</p>
                        <p style="text-align: left;">Atenciosamente,<br><img src="https://lh3.googleusercontent.com/nwCtWiJMFqjP8cdTdz_oGIRxPL3t727KfP_nTf4fk-XYogMwLy4ce2oXzbsxTowpfk1TuB86fF25bacTYLeu4WC3E_X9VS2c-zr8tzsspSgUJxyFHYjnWgdgIHPCiMKLQ33mRbWJcwuCnU6Ud1ImnVDqTpEN3XB5aHBOcOMt1rsv1vsL7UXun8htSTN79zf4sz85O23Ao-Ul1KBeTVK2tvJocYpaG4WR6aUmemE85qq0kMSd7nOC9bRjoahOA3RPV_dFPcX9XUCepYgeBSWToDoF2mPnu99cponASFhs0OOz3SoILdOwyIHTEP3oauAwst2ehulsyfQd_FY9EQNYzHbx2KgW7MbgZH4Nx5NX0CtmmNby0DexeSnSNWcBuct7hVZHiP7EOu7FK8o3WpnlsGI2tvxTXHxoCgc_nRh0gXMkFQtvLnFl7GdJLRWW64wwxyK0-4OawAXPoWO2tOF87Mm6p3oRlujCvVHv5F4EEaO4Igi8_kOU8lurqZ06C724cW3edOKXhppfKnFyff9BVGl0_yiUQ6M4Oyhf9vaqBph0GkaJ9Zy653JTWVmt4iO40jH6n6gXO0zAYwJWlntksbZRrR4HgsrFDV6U-c7KmfwFLCA_rok6Zgd4LxVTeCJqT6JcoB8-xEDN_jYUQH4StQCRS-tXqcmMcu5I5o6GimQr4WGAnrGkYMbAu37PRuMjuy3aMndBbKkPFLes2AFJGXI3=w583-h146-no?authuser=0" alt="logo" width="300" height="100"></p>
                        <blockquote>
                            <hr>
                            <h6 style="text-align: center;">N&atilde;o responda a este e-mail.<br>Este e-mail foi gerado automaticamente pela plataforma EMPRESA.<br>S&atilde;o Paulo - SP<br><br><span style="color: #000000;"><a href="https://allugaki.com/politica_privacidade" style="color: #000000;">Pol&iacute;tica de Privacidade</a> | <a href="https://allugaki.com/version-test/termos_de_uso" style="color: #000000;">Termos de Uso</a> | <a href="https://allugaki.com/suporte" style="color: #000000;">Suporte</a></span></h6>
                        </blockquote>
                        """

            text = f"""Fala {(usuarios[i]).title()}!<br><br>""" + request.form['text_area'] + carimbo

            message = text

            # add in the message body
            msg.attach(MIMEText(message, 'html'))

            # send the message via the server set up earlier
            s.send_message(msg)

            del msg

        s.quit()

        # Deletar arquivos da pasta upload
        if os.path.exists('upload/emails.txt'):
            os.remove('upload/emails.txt')

        return '<h1>Email enviado com sucesso!</h1>'


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    main()
