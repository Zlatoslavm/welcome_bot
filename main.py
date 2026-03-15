import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time  # ← ОБЯЗАТЕЛЬНО! (была пропущена раньше)

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
TOKEN = '8762440508:AAHnbNC9EcjXbb-AZxIkcddgGo3bJ-cgowY'  # ← замени!
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ФОТО С ТВОЕГО ПК
PHOTO_PATH = "welcome.png"   # ←←← ПОЛОЖИ ФОТО РЯДОМ СО СКРИПТОМ И НАЗОВИ ТАК
# Если фото в другой папке:
# PHOTO_PATH = r"C:\Users\ТвоёИмя\Pictures\welcome.jpg"
# или
# PHOTO_PATH = "/home/user/welcome.jpg"  (для Linux/Mac)
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

bot = telebot.TeleBot(TOKEN)


def delete_message_later(chat_id, message_id, delay=600):
    """Удаляет сообщение через 10 минут (600 секунд)"""
    def task():
        try:
            time.sleep(delay)
            bot.delete_message(chat_id, message_id)
        except:
            pass
    threading.Thread(target=task, daemon=True).start()


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        if new_member.is_bot:
            continue

        mention = f'<a href="tg://user?id={new_member.id}">{new_member.first_name}</a>'

        text = f"Добро пожаловать в BS Team, {mention}! 🎉\n\n" \
               f"Перед началом работы, ознакомься с информацией выше"

        # Кнопка
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(
                "МАНУАЛЫ",
                url="https://teletype.in/@bsteam/w2UZE7bcu4h"               # ← СЮДА ВСТАВЬ СВОЮ ССЫЛКУ
            )
        )

        # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
        # ОТПРАВЛЯЕМ ФОТО С ПК + текст + кнопка
        sent_msg = bot.send_photo(
            message.chat.id,
            photo=open(PHOTO_PATH, 'rb'),   # ← фото берётся прямо с твоего компьютера
            caption=text,
            parse_mode='HTML',
            reply_markup=markup
        )
        # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

        # Удаление через 10 минут
        delete_message_later(message.chat.id, sent_msg.message_id, delay=600)


print("Бот запущен и ждёт новых участников...")
bot.infinity_polling()