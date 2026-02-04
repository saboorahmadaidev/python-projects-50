import smtplib as s 

ob = s.SMTP('smtp.gmail.com', 587)
ob.ehlo()
ob.starttls()
ob.login('saboorahamd.aidev@gmail.com' , 'your_app_password_here')
subject = "Test Email from Python"
body = "This is a test email sent from a Python script."
message = f"Subject: {subject}\n\n{body}"
listadd=['saboorahmad@gmail.com',
        'saboorahmad.ml@gmail.com']
ob.sendmail('saboorahamd.aidev@gmail.com', listadd, message)
ob.quit()
