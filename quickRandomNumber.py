# -*- coding: utf-8 -*-
#QuickRandomNumber v1.1

import telebot, json
from datetime import datetime
from time import sleep
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

with open('config.json', 'r') as file:  config = json.load(file)

BOT_TOKEN = config['TOKEN']['QuickRandomNumberBot']
BOT_INTERVAL = 1
BOT_TIMEOUT = 20
WAIT_MENUPPAL = 0.16
WAIT_NAVEGACION = 0.08

def bot_polling():
    print("Starting bot polling now")

    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN)
            botactions(bot)
            bot.set_my_commands([
                telebot.types.BotCommand('/botones', 'Muestra los botones'),
            ])
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)

        except Exception as ex:
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)

        else:
            bot.stop_polling()
            print("Bot polling loop finished")
            break
#--------------------------------------------------------------------------------------------------
def showButtons(bot, chatid):
    sleep(WAIT_MENUPPAL)
    botones = ReplyKeyboardMarkup(resize_keyboard=True)
    botones.row('/LoteriaNacional')
    msg = bot.send_message(chatid, 'Selecciona una opción:', reply_markup=botones)
    #return msg
#--------------------------------------------------------------------------------------------------
def botactions(bot):

    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        botones = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Usa el comando /inicio para empezar', reply_markup=botones)

    @bot.message_handler(commands=['inicio', 'botones'])
    def cmd_iniciar(message):
        showButtons(bot, message.chat.id)

    @bot.message_handler(commands=['LoteriaNacional'])
    def cmd_nacional(message):
        sleep(WAIT_NAVEGACION)
        #numero = random.randint(0, 99999)
        now = datetime.now()
        numero = now.strftime('%f')[:5] #Microseconds. First five digits.
        print(now)
        bot.send_message(message.chat.id, 'Núm. Lotería Nacional:\n----- <b>' + numero + ' -----</b>', parse_mode="html")
        showButtons(bot, message.chat.id)
#--------------------------------------------------------------------------------------------------
bot_polling()
