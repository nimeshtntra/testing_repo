import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
TOKEN = '5405546569:AAH3sHUfC8vBmh2q23jp-e3C6DmNw823-N0'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    print( result, key, step, '+++++++++++')
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()
print('start')
bot.infinity_polling()