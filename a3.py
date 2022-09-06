from asyncio.log import logger
import base64
from distutils import errors
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import urllib.error

from click import Path

def create_message(sender, to, subject, message_text):#MIMEText を base64 エンコードする(sendmailから)
    enc = "utf-8"
    message = MIMEText(message_text.encode(enc), _charset=enc)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}

def create_message_with_attachment(sender, to, subject, message_text, file_path):#添付ファイルつきのMIMEText を base64 エンコードする(listmailから)
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    # attach message text
    enc = "utf-8"
    msg = MIMEText(message_text.encode(enc), _charset=enc)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file_path)

    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"
    main_type, sub_type = content_type.split("/", 1)
    if main_type == "text":
        with open(file_path, "rb") as fp:
            msg = MIMEText(fp.read(), _subtype=sub_type)
    elif main_type == "image":
        with open(file_path, "rb") as fp:
            msg = MIMEImage(fp.read(), _subtype=sub_type)
    elif main_type == "audio":
        with open(file_path, "rb") as fp:
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
    elif main_type == "application": #PDFを添付するため
        with open(file_path, "rb") as fp:
            msg = MIMEApplication(fp.read(), _subtype=sub_type)
    else:
        with open(file_path, "rb") as fp:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
    p = Path(file_path)
    msg.add_header("Content-Disposition", "attachment", filename=p.name)
    message.attach(msg)

    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}

def send_message(service, user_id, message):#メッセージを作成する
    try:
        sent_message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        logger.info("Message Id: %s" % sent_message["id"])
        return None
    except urllib.error.HTTPError as error:
        logger.info("An error occurred: %s" % error)
        raise error