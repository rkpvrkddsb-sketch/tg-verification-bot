from flask import Flask
import os
import telebot
import threading

# ===============================
# 🔹 Змінні середовища
BOT_TOKEN = os.environ.get("7738954223:AAGxiZQM5S11Fl-PQim0Fvuk2HcBfhnScTQ")
CHANNEL_ID = os.environ.get("-1003198292422")

if not BOT_TOKEN or not CHANNEL_ID:
    print("❌ BOT_TOKEN або CHANNEL_ID не знайдено!")
    exit(1)

# Пробуємо перетворити CHANNEL_ID на int (для приватного каналу)
try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    pass  # залишаємо як рядок для @username публічного каналу

# ===============================
# 🔹 Створюємо бота
bot = telebot.TeleBot(BOT_TOKEN)

# ===============================
# 🔹 Код бота (кнопка "Я человек")
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Я человек", callback_data="human")
    markup.add(button)
    bot.send_message(message.chat.id,
                     "Пожалуйста, подтвердите, что вы человек 👇",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "human")
def confirm(call):
    try:
        invite = bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
        link = invite.invite_link if hasattr(invite, "invite_link") else invite["invite_link"]
        bot.send_message(call.message.chat.id,
                         f"✅ Проверка пройдена!\nВот ссылка на канал:\n{link}")
        bot.answer_callback_query(call.id, "Вы подтверждены как человек!")
    except Exception as e:
        bot.send_message(call.message.chat.id,
                         "⚠️ Ошибка при создании ссылки. Сообщите админу.")
        print("Ошибка при создании invite link:", e)

# ===============================
# 🔹 Flask для порту
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# ===============================
# 🔹 Запускаємо polling у фоні
def run_bot():
    bot.polling(non_stop=True)

threading.Thread(target=run_bot).start()

# ===============================
# 🔹 Запускаємо Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
