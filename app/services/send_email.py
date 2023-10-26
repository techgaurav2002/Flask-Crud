import smtplib

def send_otp_email(email, otp):
    # Replace these with your email server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "hakergaurav.mkp2000@gmail.com"
    smtp_password = "bpjyynjzwdvmekix"

    from_email = "hakergaurav.mkp2000@gmail.com"
    to_email = email

    subject = "One-Time Password (OTP) for Registration"
    message = f"Your OTP for registration is: {otp}"

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{message}")

        # Close the connection
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False
    

def send_forgot_links(email, links):
    # Replace these with your email server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "hakergaurav.mkp2000@gmail.com"
    smtp_password = "bpjyynjzwdvmekix"

    from_email = "hakergaurav.mkp2000@gmail.com"
    to_email = email

    subject = "Forgot Password Link"
    message = f"Your forgot-password link is : {links}"

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{message}")

        # Close the connection
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False