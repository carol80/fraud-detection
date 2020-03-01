import pandas as pd
import smtplib

SenderAddress = "yobro9594246827@gmail.com"
password = "thetimesofindia"

e = pd.read_excel("Email.xlsx")
Messages = e.iloc[0:17,0]
email = 'abdulshahlatiiffkhamura@gmail.com'
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SenderAddress, password)
count = 0
for msg in Messages:
    count += 1
    msg = msg
    subject = "Test Message No: {}".format(count)
    body = "Subject: {}\n\n{}".format(subject,msg)
    server.sendmail(SenderAddress, email, body)
server.quit()