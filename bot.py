import os
import telebot

TOKEN = os.environ.get("7738954223:AAGxiZQM5S11Fl-PQim0Fvuk2HcBfhnScTQ")
CHANNEL_ID = os.environ.get("1335337196")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Я человек", callback_data="human")
    markup.add(button)
    bot.send_message(message.chat.id, "Пожалуйста, подтвердите, что вы человек 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "human")
def confirm(call):
    # створюємо одноразове запрошення
    try:
        invite_link = bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
        bot.send_message(call.message.chat.id, f"✅ Проверка пройдена!\nВот ссылка для входа в канал:\n{invite_link.invite_link}")
        bot.answer_callback_query(call.id, "Вы подтверждены как человек!")
    except Exception as e:
        bot.send_message(call.message.chat.id, "⚠️ Ошибка при создании ссылки. Сообщите администратору.")
        print(e)

# нескінченний цикл — щоб бот працював
bot.polling(non_stop=True)

