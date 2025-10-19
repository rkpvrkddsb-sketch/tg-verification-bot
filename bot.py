import os
import telebot
from flask import Flask
import threading

# ===============================
# 🔹 ТУТ НЕ ВПИСУЄМО токен і ID безпосередньо
# Render підхоплює їх зі змінних середовища

BOT_TOKEN = os.environ.get("BOT_TOKEN")      # <-- додати BOT_TOKEN у Render Environment
CHANNEL_ID = os.environ.get("CHANNEL_ID")    # <-- додати CHANNEL_ID у Render Environment

# ===============================
# 🔹 Перевірка змінних
print("DEBUG: BOT_TOKEN =", repr(BOT_TOKEN))
print("DEBUG: CHANNEL_ID =", repr(CHANNEL_ID))

if not BOT_TOKEN or not CHANNEL_ID:
    print("❌ BOT_TOKEN або CHANNEL_ID не знайдено!")
    exit(1)

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    pass  # залишаємо як рядок для публічного каналу (@username)

# ===============================
# 🔹 Створюємо бота
bot = telebot.TeleBot(BOT_TOKEN)

# ===============================
# 🔹 Кнопка "Я человек"
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
                         f"✅ Проверка пройдена!\nВот ссылка для входа в канал:\n{link}")
        bot.answer_callback_query(call.id, "Вы подтверждены как человек!")
    except Exception as e:
        bot.send_message(call.message.chat.id,
                         "⚠️ Ошибка при создании ссылки. Сообщите админу.")
        print("Ошибка при создании invite link:", e)

# ===============================
# 🔹 Flask для Render порту
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# ===============================
# 🔹 Polling у фоні
def run_bot():
    bot.polling(non_stop=True)

threading.Thread(target=run_bot).start()

# ===============================
# 🔹 Запуск Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
