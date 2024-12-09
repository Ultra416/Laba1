import telebot

# Токен
TOKEN = "8172214939:AAE-If9yql9uCfG6wEvvqVyG3cFbC54TCiU"

# створення бота
bot = telebot.TeleBot(TOKEN)

# повторює Кожне повідомлення 
@bot.message_handler(func = lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# запуск бота
print("Бот запущено...")
bot.infinity_polling()
