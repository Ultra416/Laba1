import telebot

# Токен, отриманий від BotFather
TOKEN = "8172214939:AAE-If9yql9uCfG6wEvvqVyG3cFbC54TCiU"

# Створюємо об'єкт бота
bot = telebot.TeleBot(TOKEN)

# Обробляємо команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я ехо-бот. Напиши мені щось, і я повторю!")

# Обробляємо будь-які текстові повідомлення
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запускаємо бота
print("Бот запущено...")
bot.infinity_polling()