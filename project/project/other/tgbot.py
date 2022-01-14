from telepot.loop import MessageLoop
import telepot
import time
import sqlite3
from dotenv import load_dotenv, find_dotenv
import os


def condb():
    conn = sqlite3.connect("/spgr2/instance/database.db")
    cursor = conn.cursor()
    cursor.execute('select tg_chat_id,wallet,pending_amount from users where tg_chat_id IS NOT NULL')
    result = cursor.fetchall()
    return result
    conn.close()


load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")
bot = telepot.Bot(TOKEN)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    chat_id = str(chat_id)
    if msg['text'] == '/info':
        bot.sendMessage(chat_id, 'Your telegram user id is: %s, please give id to ShopEmployee' % (chat_id))

    if msg['text'] == '/balance':
        values = condb()
        for row in values:
            if chat_id == row[0]:
                s = row[1] - row[2]
                bot.sendMessage(chat_id, 'you balance is: %s euro' % (s))
                break
        else:
            bot.sendMessage(chat_id, 'please bind your telegram username firstly')


MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(5)
