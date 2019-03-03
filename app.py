import os
import sys
import errno
import logging
from django.http import HttpResponse
import watermarker, chatter
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, VideoMessage, AudioMessage
)

app = Flask(__name__)
application = app

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', 'e3383f17a51ccf12a48159c30d89f749')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN',
                                 'wChZjVe8c2HC9jAAZKUbw7UJlvuqHC8UpMa4F1rGcdErToBxGZtWG7hXSv1Z1RdtqjQY6HyaghQorEosmIzbDkQdb4ec/fjWle1lW4enYy4Qiss9alTq46dj3YGmTU7y9VK2jFQACJ0skvlLMzhtHAdB04t89/1O/w1cDnyilFU=')

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'img')


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

def index(request):
    return HttpResponse(https://qr-official.line.me/M/XYrdE8dL2o.png)
    
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=(TextMessage))
def message_text(event):
    q = event.message.text
    res = chatter.chatmachine(q)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=event.message.text),
            TextSendMessage(text=res)
        ]
    )


@handler.add(MessageEvent, message=(ImageMessage))
def handle_content_message(event):
    script_dir = os.path.dirname(__file__)
    message_content = line_bot_api.get_message_content(event.message.id)
    ext = ".png"

    rel_path = os.path.join("static/temp/", event.message.id + ext)
    file_path = os.path.join(script_dir, rel_path)

    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    result_path = os.path.join(script_dir, "static/result", event.message.id + ext)
    watermark1 = os.path.join(script_dir, "static/", "watermark.png")

    with open(os.path.join(script_dir, "static/log.log"), 'w+') as f:
        f.write(result_path)

    watermarker.watermark_with_transparency(file_path, result_path, watermark1, position=(7, 7))

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Iki hasile:'),
            ImageSendMessage(
                original_content_url=request.host_url + "static/result/" + event.message.id + ext,
                preview_image_url=request.host_url + "static/result/" + event.message.id + ext
            )
        ])


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
