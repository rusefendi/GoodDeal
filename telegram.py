import misc
import requests

# your Telegram bot token
token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'


def send_message(chat_id, text):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


# requested for sending messages
def get_chat_id():
    data = get_updates()

    chat_id = data['result'][-1]['message']['chat']['id']

    return chat_id


def post(data):
    text = data['title'] + '\n' + data['price'] + '\n' + data['metro'] + '\n' + data['url']

    send_message(get_chat_id(), text)
