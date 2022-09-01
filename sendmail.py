"""
Send E-Mail with GMail.

Usage:
  sendmail.py <sender> <to> <subject> <message_text_file_path>  [--attach_file_path=<file_path>] [--cc=<cc>]
  sendmail.py -h | --help
  sendmail.py --version

Options:
  -h --help     Show this screen.
  --version     Show version. 
  --attach_file_path=<file_path>     Path of file attached to message.
  --cc=<cc>     cc email address list(separated by ','). Default None.
"""
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from pathlib import Path

from email.mime.multipart import MIMEMultipart
import mimetypes
from apiclient import errors
from gmail_credential import get_credential
from docopt import docopt
import logging

from email import message
from email.errors import MultipartInvariantViolationDefect

import json
import io
import csv

import os
from unicodedata import name
import img2pdf
from PIL import Image

logger = logging.getLogger(__name__)

def list_labels(service, user_id): #listmailから
    """
    label のリストを取得する
    """
    labels = []
    response = service.users().labels().list(userId=user_id).execute()
    return response["labels"]

def decode_base64url_data(data): #listmailから
    """
    base64url のデコード
    """
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode("UTF-8")
    return decoded_message

def list_message(service, user_id): #listmailから
    messages = []
    try:
        message_ids = (
            service.users()
            .messages()
            .list(userId=user_id, maxResults=1, q='is:unread')#, maxResults=count, q=query, labelIds=label_ids) #用途により取捨選択
            .execute()
        )
        #print(message_ids)
        if message_ids["resultSizeEstimate"] == 0:#当てはまるメールがない時
            logger.warning("no result data!")
            return []
        # message id を元に、message の内容を確認
        for message_id in message_ids["messages"]:
            message_detail = (#メールの情報を取得(id(メール１件ずつ一意に割り振られている), 宛先, 件名など)
                service.users()
                .messages()
                .get(userId="me", id=message_id["id"])
                .execute()
            )
            # print(message_detail)
            message = {}
            message["id"] = message_id["id"] #メッセージのidを取得
            # 単純なテキストメールの場合
            if 'data' in message_detail['payload']['body']: #[payload]の中の[body](本文)
                message["body"] = decode_base64url_data(
                    message_detail["payload"]["body"]["data"]
                )
            # html メールの場合、plain/text のパートを使う
            else:
                parts = message_detail['payload']['parts']
                parts = [part for part in parts if part['mimeType'] == 'text/plain']
                message["body"] = decode_base64url_data(
                    parts[0]['body']['data']
                    )
            # payload.headers[name: "Subject"]
            for header in message_detail["payload"]["headers"]:
                if header["name"] == "Subject":
                    message["subject"] = header["value"]
            # print(message["subject"])
            # payload.headers[name: "From"]
            for header in message_detail["payload"]["headers"]:
                if header["name"] == "From":
                    message["from"] = header["value"]
            logger.info(message_detail["snippet"])
            # if message["subject"] == "特定の件名":
            messages.append(message)
        return messages
    except errors.HttpError as error:
        print("An error occurred: %s" % error)

def remove_labels(service, user_id, messages, remove_labels): #listmailから
    """
    ラベルを削除する。既読にするために利用(is:unread ラベルを削除すると既読になる）
    list_mailを実行しただけでは未読が既読にはならない
    """
    message_ids = [message["id"] for message in messages]
    labels_mod = {
        "ids": message_ids,
        "removeLabelIds": remove_labels,
        "addLabelIds": [],
    }
    # import pdb;pdb.set_trace()
    try:
        message_ids = (
            service.users()
            .messages()
            .batchModify(userId=user_id, body=labels_mod)
            .execute()
        )
    except errors.HttpError as error:
        print("An error occurred: %s" % error)

def convert2pdf(output,input): #pngをpdfに変換する
    with open(output,"wb") as f:
        f.write(img2pdf.convert(input))

def create_message(sender, to, subject, message_text, cc=None):
    """
    MIMEText を base64 エンコードする
    """
    enc = "utf-8"
    message = MIMEText(message_text.encode(enc), _charset=enc)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    if cc:
        message["Cc"] = cc
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}


def create_message_with_attachment(
    sender, to, subject, message_text, file_path, cc=None
):
    """
    添付ファイルつきのMIMEText を base64 エンコードする
    """
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    if cc:
        message["Cc"] = cc
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
    else:
        with open(file_path, "rb") as fp:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
    p = Path(file_path)
    msg.add_header("Content-Disposition", "attachment", filename=p.name)
    message.attach(msg)

    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": encode_message.decode()}


def send_message(service, user_id, message):
    """
    メールを送信する

    Parameters
    ----------
    service : googleapiclient.discovery.Resource
        Gmail と通信するためのリソース
    user_id : str
        利用者のID
    message : dict
        "raw" を key, base64 エンコーディングされた MIME Object を value とした dict

    Returns
    ----------
    なし
    """
    try:
        sent_message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        logger.info("Message Id: %s" % sent_message["id"])
        return None
    except errors.HttpError as error:
        logger.info("An error occurred: %s" % error)
        raise error


#  メイン処理
def main(): #sender, to, subject, message_text, attach_file_path, cc=None):
    # アクセストークンの取得とサービスの構築
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    #受信したメールの情報の取得
    labels = list_labels(service, "me")
    messages = list_message(service, "me")

    if messages[0]['subject'] == "地図取得":
        #特定の件名だったら翔んで埼玉or千葉
        address = messages[0]['body']
        print(address)
        sender = "nozomi.shimonishi@gmail.com" #<<<インターンの共通アカウントを入れる
        to = messages[0]['from']
        subject = "Re:地図取得"
        message_text = messages[0]['body']
        attach_file_path = "output.pdf" #<<<ここにスクショをPDFに変換したものを入れる
        message = create_message_with_attachment(
            sender, to, subject, message_text, attach_file_path, cc=None
        )
        # メール送信
        send_message(service, "me", message)


    else:
        #特定の件名じゃなかったら既読にして終わり
        unread_label_ids = [label["id"] for label in labels if label["name"] == "UNREAD"]
        remove_labels(service, "me", messages, remove_labels=unread_label_ids)
        print("地図取得のメールではない")
        exit()

    # unread label
    unread_label_ids = [label["id"] for label in labels if label["name"] == "UNREAD"]
    # remove labels form messages
    remove_labels(service, "me", messages, remove_labels=unread_label_ids)

    logger.info(json.dumps(messages, ensure_ascii=False))

    # if messages:
    #     return json.dumps(messages, ensure_ascii=False)
    # else:
    #     return None

# プログラム実行部分
if __name__ == "__main__":
    """"
    arguments = docopt(__doc__, version="0.1")
    sender = arguments["<sender>"]#自分
    to = arguments["<to>"]#listmailからmessages[0]['from']で受け取る
    cc = arguments["--cc"]#不要
    subject = arguments["<subject>"]#Re:地図取得
    message_text_file_path = arguments["<message_text_file_path>"]#messages[0]['body]に書かれている住所
    attach_file_path = arguments["--attach_file_path"]#convert2pdfで作成したPDFファイル

    logging.basicConfig(level=logging.DEBUG)

    with open(message_text_file_path, "r", encoding="utf-8") as fp:
        message_text = fp.read()
    """

    main(
        # sender=sender,
        # to=to,
        # subject=subject,
        # message_text=message_text,
        # attach_file_path=attach_file_path,
        # cc=cc,
    )
