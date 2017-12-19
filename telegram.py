import misc
import requests

# your Telegram bot token
token = misc.token
chat_id = misc.chat_id
URL = 'https://api.telegram.org/bot' + token + '/'


def send_message(text):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def post(data):
    text = data['title'] + '\n' + data['price'] + '\n' + data['metro'] + '\n' + data['url']

    send_message(text)
