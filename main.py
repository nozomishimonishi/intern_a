import logging
import os.path
from googleapiclient.discovery import build
from gmail_credential import get_credential

import json
import re
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import a1
import a2
import a3
import a4
import a5
# import a6
import a7
import a8
import a9
import a10

import slackweb



service = Service(executable_path=ChromeDriverManager().install())
logger = logging.getLogger(__name__)
slack = slackweb.Slack(url="https://hooks.slack.com/services/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")

def main():
    creds = get_credential()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    #受信したメールの情報の取得
    labels = a1.list_labels(service, "me")
    messages = a1.list_message(service, "me")
    
    while(messages!=[]):
        #未読を既読にする
        unread_label_ids = [label["id"] for label in labels if label["name"] == "UNREAD"]
        a1.remove_labels(service, "me", messages, remove_labels=unread_label_ids)

        sender = "ohg.summer.intern24a@gmail.com" #<<<インターンの共通アカウントを入れる
        #to = messages[0]['from'] #<<<送り返す
        to = re.search(r'<(.+)>',messages[0]['from']).group(1) #メールアドレスだけを取り出す

        if messages[0]['subject'] == "地図取得":
            attach_file_path = None
            #subject = None
            message_text = messages[0]['body']
            #特定の件名だったら埼玉or千葉
            address = messages[0]['body']
            #print(address)
            output = "output_send.pdf"

            if("さいたま") in address:
                if(a10.saitama(address)==False):
                    subject = "エラー"
                    message_text = "存在しない住所です。"
                    message = a9.create_htmlmessage(sender,to,subject,message_text)
                    slack.notify(text="エラー発生しました")
                else:
                    subject = "取得成功"
                    input1 = "埼玉道路.png"
                    input2 = "埼玉下水.png"
                    a2.convert2pdf(output,input1,input2)
                    attach_file_path =  os.path.abspath("./"+output)
                    message = a3.create_message_with_attachment(sender, to, subject,message_text,attach_file_path)
                    slack.notify(text="成功❤️")
            elif ("千葉市") in address:
                road = a8.chiba_jusho_douro(address)
                gesui = a7.chiba_jusho_gesui(address)
                if(a5.chiba_road(road[0],road[1],road[2]))==True:
                    input1 = "千葉道路.png"
                    if(a4.chiba_gesui(gesui[0],gesui[1],gesui[2],gesui[3])==True):#両方取得できた
                        input2 = "千葉下水.png"
                        #pngをpdfに変換する
                        a2.convert2pdf(output,input1,input2)
                        #メール送信準備
                        subject = "取得成功"
                        message_text = messages[0]['body']
                        attach_file_path =  os.path.abspath("./"+output) #<<<ここにスクショをPDFに変換したものを入れる（相対パスを入力する！！！！）
                        message = a3.create_message_with_attachment(sender, to, subject,message_text,attach_file_path)
                        slack.notify(text="成功❤️")
                    else:#道路だけ
                        input1 = "千葉道路.png"
                        a2.convert2pdf_1(output,input1)
                        subject = "エラー"
                        message_text = "下水のPDFが取得できていません。"
                        attach_file_path =  os.path.abspath("./"+output)
                        message = a3.create_message_with_attachment(sender,to,subject,message_text,attach_file_path)
                        slack.notify(text="下水のPDFが取得できていません。")
                elif(a4.chiba_gesui(gesui[0],gesui[1],gesui[2],gesui[3])==False):#下水だけ
                    input1 = "千葉下水.png"
                    a2.convert2pdf_1(output,input1)
                    subject = "エラー"
                    message_text="道路のPDFが取得できていません。"
                    attach_file_path =  os.path.abspath("./"+output)
                    message = a3.create_message_with_attachment(sender,to,subject,message_text,attach_file_path)
                    slack.notify(text="道路のPDFが取得できていません。")
                else:#両方取得できなかった
                    #存在しない住所
                    subject = "エラー"
                    message_text = "存在しない住所です。"
                    message = a9.create_htmlmessage(sender,to,subject,message_text)
                    slack.notify(text="存在しない住所です。")
            else: #さいたま市か千葉市じゃない時
                message = a9.create_htmlmessage(sender, to,'エラー', '対象地域外です。')
                slack.notify(text="存在しない住所です。")
                # a3.send_message(service, "me", msg)

            # if attach_file_path != None:
            # # メール本文の作成
            #     message = a3.create_message_with_attachment(
            #     sender, to, subject, message_text, attach_file_path
            # )
            # else:
            #     message = a3.create_message(
            #         sender, to, subject, message_text
            #     )
            # メール送信

            a3.send_message(service, "me", message)
        else:
            #特定の件名じゃなかったら既読にして終わり
            slack.notify(text="件名「地図取得」で送信して欲しいです。")

        labels = a1.list_labels(service, "me")
        messages = a1.list_message(service, "me")
        logger.info(json.dumps(messages, ensure_ascii=False))

    # if messages:
    #     return json.dumps(messages, ensure_ascii=False)
    # else:
    #     return None

# プログラム実行部分
if __name__ == "__main__":
    main()