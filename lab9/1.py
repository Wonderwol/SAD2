def send_message(connection_type, to, message, message_type):
    print(f"Connecting to {connection_type} server...")
    print(f"Sending {message_type} to {to} with message '{message}'...")
    print(f"{message_type} sent.")


def send_email(to, subject, body):
    send_message("SMTP", to, body, "email")


def send_sms(to, message):
    send_message("SMS", to, message, "SMS")
