from flask import Flask, render_template, request
# from flask_mail import Mail, Message
from email.message import EmailMessage
import ssl
import smtplib

app= Flask(__name__)
# mail=Mail(app)


# app.config['MAIL_SERVER']= 'smtp.google.com'
# app.config['MAIL_PORT']= 465
# app.config['MAIL_USERNAME']= 'patilprajwal52@gmail.com'
# app.config['MAIL_PASSWORD']= 'xnvvgtqezwmdfnst'
# app.config['MAIL_USE_SSL']= True

sender = 'patilprajwal52@gmail.com'
password = 'xnvvgtqezwmdfnst'

subject = 'Registration Successful!!'
body = """
        Your Account Registration is Successful and you're good to go!!
        Happy Shopping!
        """

em = EmailMessage()
em['From'] = sender

em['Subject'] = subject
em.set_content(body)
context = ssl.create_default_context()

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/result", methods=['POST', 'GET'])
def res():
    if request.method == 'POST':
        receiver = request.form.get("email")
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, em.as_string())
        return render_template("result.html", res="Success")
    else:
        return render_template("result.html", res="Failure!!")

if __name__ == '__main__':
    app.run(debug=True)