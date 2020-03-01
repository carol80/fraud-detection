import pandas as pd
import smtplib

SenderAddress = "yobro9594246827@gmail.com"
password = "thetimesofindia"

e = pd.read_excel("Email.xlsx")
emails = e['Emails'].values
email = 'abdulshahlatiiffkhamura@gmail.com'
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SenderAddress, password)
msg = "Chal raha hai bantai!!!"
subject = "Sabooo pachas!!"
body = "Subject: {}\n\n{}".format(subject,msg)
# for email in emails:
#     server.sendmail(SenderAddress, email, body)
# server.quit()
for i in range(0,5):
    server.sendmail(SenderAddress, email, body)