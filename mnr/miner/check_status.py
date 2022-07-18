import requests
from bs4 import BeautifulSoup as bs
import lxml
import urllib3
import telebot
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import config
import control_miner

def get_data():
    """Get device data function"""
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
                        ',application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/96.0.4664.110 Safari/537.36',
            'Referer': 'https://192.168.31.189/cgi-bin/luci'}

    s = requests.session()
    login_payload = {'luci_username': 'admin', 'luci_password': 'b34v5er8'}
    s.post(config.URL, data=login_payload, headers=headers, verify=False)
    req = s.get(config.STATUS_URL)
    src = req.text
    soup = bs(src, "lxml")

    vent_in = soup.find('div', id='cbi-table-1-fanspeedin').text.strip()  # fan in speed
    vent_out = soup.find('div', id='cbi-table-1-fanspeedout').text.strip()  # fan out speed
    temp_1 = soup.find('div', id='cbi-table-1-temp').text.strip()  # temp1 
    temp_2 = soup.find('div', id='cbi-table-2-temp').text.strip()  # temp1
    temp_3 = soup.find('div', id='cbi-table-3-temp').text.strip()  # temp1
    mhs_av = soup.find('div', id='cbi-table-1-mhsav').text.strip()  # average mh amount
    elapsed_time = soup.find('div', id='cbi-table-1-elapsed').text.strip()  # elapsed time

    return {
            'vent_in':vent_in, 'vent_out':vent_out, 
            'temp_1':temp_1, 'temp_2':temp_2, 'temp_3':temp_3,
            'mhs_av': mhs_av, 'elapsed_time':elapsed_time
            }


# TELEGRAM BOT PART
bot = telebot.TeleBot(config.TOKEN)


def greetings(message='menu'):
    # greetings message
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    status_item = telebot.types.KeyboardButton(config.STATUS_MINER)
    run_item = telebot.types.KeyboardButton(config.RUN_MINER)
    stop_item = telebot.types.KeyboardButton(config.STOP_MINER)
    markup.add(status_item, run_item, stop_item)
    bot.send_message(config.CHAT_ID, text=message, reply_markup=markup)


def stop_miner(message):
    # send stop command to miner
    if message.text == config.YES_MESSAGE:
        bot.send_message(message.chat.id, 'Turning off miner')
        control_miner.main(run=False)
    greetings()


def start_miner(message):
    # send start command to miner
    if message.text == config.YES_MESSAGE:
        bot.send_message(message.chat.id, 'Turning on miner')
        control_miner.main(run=True)
    greetings()


@bot.message_handler(commands=['start'])
def start(message):
    greetings('I have a few commands...')


@bot.message_handler(content_types=['text'])
def get_menu(message):
    # get status info
    if message.text == config.STATUS_MINER:
        try:
            data = get_data()  # get miner data
            text = ''
            for each in data:
                text = text +  f'{each}: {data[each]}\n'
        except requests.exceptions.ConnectionError:
            text = 'Miner is offline. Check connection status'
        bot.send_message(message.chat.id, text)
    # run miner
    elif message.text == config.RUN_MINER:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        run_item = telebot.types.KeyboardButton(config.YES_MESSAGE)
        cancel_item = telebot.types.KeyboardButton(config.CANCEL_MESSAGE)
        markup.add(run_item, cancel_item)
        msg = bot.send_message(message.chat.id, 'Do u want to start miner?', reply_markup=markup)
        bot.register_next_step_handler(msg, start_miner)
        
    # stop miner 
    elif message.text == config.STOP_MINER:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        run_item = telebot.types.KeyboardButton(config.YES_MESSAGE)
        cancel_item = telebot.types.KeyboardButton(config.CANCEL_MESSAGE)
        markup.add(run_item, cancel_item)
        msg = bot.send_message(message.chat.id, 'Do u really want to stop miner?', reply_markup=markup)
        bot.register_next_step_handler(msg, stop_miner)

    elif message.text == 'Cancel':
        greetings()


bot.polling(True)