# 架設伺服器(常用：flask, django)
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# access token # secret
line_bot_api = LineBotApi('s+gFlUVJlVgieWTDQwXmSRSHoTv5Axd2WfcLG0uZHvnCdbWoLMttpRsDiBytKDQ5rerevhEAWBlEAz7ZVhy30DgxDlhSI+TTucvE2YIcjagHahablv5q7f3Jv6spuU2fLKXw+xBlRq5HEVYgt6Y/AQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('321415710a1e10b9aa11fab2e2f6cc5d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) # 回復使用者傳來的訊息


if __name__ == "__main__": # 不希望import的時候就執行程式碼，確定檔案是被執行而不是被載入
    app.run()