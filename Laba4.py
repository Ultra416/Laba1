import telebot

# Токен
TOKEN = "8172214939:AAE-If9yql9uCfG6wEvvqVyG3cFbC54TCiU"

# створення бота
bot = telebot.TeleBot(TOKEN)

# початок взаємодії командою /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я ехо-бот. Напиши мені щось, і я повторю!")

# повторює Кожне повідомлення 
@bot.message_handler(func = lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# запуск бота
print("Бот запущено...")
bot.infinity_polling()
