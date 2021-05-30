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
    msg = event.message.text
    s = '抱歉我看不懂hehe'

    if msg == '你好':
        s = '小然好！今天想吃什麼？選項有：和牛涮、屋馬、河童'
    elif msg == '和牛涮':
        s = '卡架！'
    elif msg == '屋馬':
        s = '卡架！'
    elif msg == '河童':
        s = '想得美:P'
    elif msg == '吃飽了':
        s = '那你今天想要一起做什麼事？選項有：夜衝看夜景、看電影、在家裡吃鹹酥雞打電動'
    elif msg == '夜衝看夜景':
        s = '好ㄚ上車吧！'
    elif msg == '看電影':
        s = '那好吧:( 你選'
    elif msg == '在家裡吃鹹酥雞打電動':
        s = '好！那還要配瓜瓜奶！'
    elif msg == '開心':
        s = '那你今天幸福嗎？'
    elif msg == '幸福':
        s = '庭亦也幸福～謝謝小然的陪伴！比起生日快樂，更希望你身體健康、天天開心哦love you 3000'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s)) # 回復使用者傳來的訊息


if __name__ == "__main__": # 不希望import的時候就執行程式碼，確定檔案是被執行而不是被載入
    app.run()