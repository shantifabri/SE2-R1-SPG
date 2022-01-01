from telepot.loop import MessageLoop
import telepot
import time
import sqlite3
from dotenv import load_dotenv, find_dotenv
import os

conn = sqlite3.connect('/project/instance/database.db')
cursor = conn.cursor()
cursor.execute('select tgusername,wallet,pending_amount from users where tgusername IS NOT NULL')
values = cursor.fetchall()
conn.close()

load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")
bot = telepot.Bot(TOKEN)

def handle(msg):
    username = msg['from']['username']
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(username)

    if msg['text'] == '/balance':
        for row in values:

            if username == row[0]:
                s = row[1]-row[2]
                bot.sendMessage(chat_id, 'you balance is: %s euro' % (s))
                break
        else:
            bot.sendMessage(chat_id, 'please bind your telegram username firstly')

MessageLoop(bot, handle).run_as_thread()


while 1:
    time.sleep(5)