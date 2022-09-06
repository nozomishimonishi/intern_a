from email import message
from email.errors import MultipartInvariantViolationDefect
import pickle
import base64
import json
import io
import csv
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
from apiclient import errors
import logging
from docopt import docopt
from gmail_credential import get_credential
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)
service = Service(executable_path=ChromeDriverManager().install())

def list_labels(service, user_id): #ラベルのリストを取得(listmailから)
    labels = []
    response = service.users().labels().list(userId=user_id).execute()
    return response["labels"]

def decode_base64url_data(data): #base64urlのデコード(listmailから)
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode("UTF-8")
    return decoded_message

def list_message(service, user_id): #メールの情報を取り出す(listmailから)  
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
            #print(message_detail)
            message = {}
            message["id"] = message_id["id"] #メッセージのidを取得
            # 単純なテキストメールの場合
            if 'data' in message_detail['payload']['body']: #[payload]の中の[body](本文)
                message["body"] = decode_base64url_data(
                    message_detail["payload"]["body"]["data"]
                )
            # partsの中のmimeTypeがalternativeの場合も対応させる。

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

def remove_labels(service, user_id, messages, remove_labels): #既読にする(listmailから)
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
