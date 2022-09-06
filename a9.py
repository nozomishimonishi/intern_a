import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create_htmlmessage(sender, to, subject, message_text):#MIMEText を base64 エンコードする(sendmailから)
    msg = MIMEMultipart('altarnative')
    msg["to"] = to
    msg["from"] = sender
    msg["subject"] = subject

    html = """
    <html>
        <head></head>
        <body>
            <p style='font-size:20.0pt;font-family:Meiryo'>"""
    html += message_text
    html += """</p>
            <p style 0 'font-size:10.0pt; font-family:Meiryo; color:#ff4500'>対象地域は千葉市かさいたま市のみです。</p>
    </html>
    """

    # part1 = MIMEText(message_text,'plain')
    part2 = MIMEText(html,'html')
    msg.attach(part2)

    encode_message = base64.urlsafe_b64encode(msg.as_bytes())
    return {"raw": encode_message.decode()}