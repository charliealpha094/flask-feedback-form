# Done by Carlos Amaral (2021/01/10)

import smtplib
from email.mime.text import MIMEText

def sendmail(customer, dealer, model, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'a9c9c4fc9e9b10'
    password = '96e3a83d1e968b'
    message = f"<h3>New feedback submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Model: {model}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'carlosamaral94@gmail.com'
    receiver_email = 'erosolympus200@protonmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Mitsubishi Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
