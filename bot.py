import os
import telebot
from flask import Flask
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    print("❌ BOT_TOKEN або CHANNEL_ID не знайдено!")
    exit(1)

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    pass

bot = telebot.TeleBot(BOT_TOKEN)

# ===============================
# 🔹 Автоматична клавіатура з кнопкою "Старт"
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Я человек")  # Кнопка на клавіатурі
    bot.send_message(message.chat.id,
                     "Пожалуйста, подтвердите, что вы человек 👇",
                     reply_markup=markup)

# ===============================
# 🔹 Обробка натискання кнопки "Я человек"
@bot.message_handler(func=lambda message: message.text == "Я человек")
def confirm(message):
    try:
        invite = bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
        link = invite.invite_link if hasattr(invite, "invite_link") else invite["invite_link"]
        bot.send_message(message.chat.id,
                         f"✅ Проверка пройдена!\nВот ссылка для входа в канал:\n{link}")
    except Exception as e:
        bot.send_message(message.chat.id,
                         "⚠️ Ошибка при создании ссылки. Сообщите админу.")
        print("Ошибка при создании invite link:", e)

# ===============================
# 🔹 Flask для Render
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

def run_bot():
    bot.polling(non_stop=True)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
