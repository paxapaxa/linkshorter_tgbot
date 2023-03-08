import pyshorteners
import telebot
import config
import qrcode
from io import BytesIO

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    sti = open('static/zdarova.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                     "Привет! Я бот для сокращения ссылок! Просто вышли мне ссылку, которую нужно сократить, "
                     "и я все сделаю :)")


@bot.message_handler(content_types=['text'])
def short(message):
    try:
        s = pyshorteners.Shortener()
        shor = s.tinyurl.short(message.text)
        img = qrcode.make(shor)
        photo = BytesIO()
        photo.name = 'image.png'
        img.save(photo, 'png')
        photo.seek(0)
        bot.send_photo(message.chat.id, photo, caption=shor)
    except BaseException:
        bot.send_message(message.chat.id, "Что-то пошло не так :( Отправьте ссылку повторно, пожалуйста")


bot.polling(none_stop=True)
