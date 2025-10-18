# bot.py
import os
import telebot

# 🔹 Беремо токен та ID каналу зі змінних середовища
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Перевірка наявності токена та каналу
if not BOT_TOKEN or not CHANNEL_ID:
    print("❌ BOT_TOKEN або CHANNEL_ID не знайдено. Додай їх у Environment Variables!")
    exit(1)

# Перетворюємо CHANNEL_ID на int, якщо це приватний канал
try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    # залишаємо як рядок для @username публічного каналу
    pass

# Створюємо об'єкт бота
bot = telebot.TeleBot(BOT_TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("Я человек", callback_data="human")
    markup.add(button)
    bot.send_message(message.chat.id,
                     "Пожалуйста, подтвердите, что вы человек 👇",
                     reply_markup=markup)

# Обробка натискання кнопки
@bot.callback_query_handler(func=lambda call: call.data == "human")
def confirm(call):
    try:
        # Створюємо одноразове посилання для входу в канал
        invite = bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
        link = invite.invite_link if hasattr(invite, "invite_link") else invite["invite_link"]
        bot.send_message(call.message.chat.id,
                         f"✅ Проверка пройдена!\nВот ссылка для входа в канал:\n{link}")
        bot.answer_callback_query(call.id, "Вы подтверждены как человек!")
    except Exception as e:
        bot.send_message(call.message.chat.id,
                         "⚠️ Ошибка при создании ссылки. Сообщите админу.")
        print("Ошибка при создании invite link:", e)

# Запуск бота
bot.polling(non_stop=True)
