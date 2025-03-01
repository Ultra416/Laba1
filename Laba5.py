# бібліотеки:
import telebot # бот в телеграмі
import random  # генератор ймовірностей
import string  # маніпуляція з текстом
import json    # маніпуляція з файлами json

# створення вашого бота
TOKEN = "7274151929:AAHkjqiAnVMEL3WMI-FSzGS1nMv4maztn1k"
bot = telebot.TeleBot(TOKEN)

# файл для зберігання паролів
DATA_FILE = "passwords.json"

# завантаження або створення бази паролів
try:
    with open(DATA_FILE, "r") as file:
        passwords = json.load(file)
except FileNotFoundError: 
    passwords = {}

# команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привіт! Я бот для управління паролями. Доступні команди:\n"
                          "/add - додати новий пароль\n"
                          "/get - отримати пароль\n"
                          "/generate - згенерувати надійний пароль")

# додавання нового пароля
@bot.message_handler(commands=['add'])
def add_password(message):
    msg = bot.reply_to(message, "Введіть назву сервісу:")
    bot.register_next_step_handler(msg, get_service_name) # виклик функції(get_service_name) після повідомлення(msg)

def get_service_name(message):
    service = message.text
    if service in passwords:
        bot.reply_to(message, "Пароль для цього сервісу вже існує. Використовуйте іншу назву.")
    else:
        msg = bot.reply_to(message, "Введіть ваш пароль:")
        bot.register_next_step_handler(msg, lambda m: save_password(m, service)) # lambda використанна для перенесення декількох повідомлень

def save_password(message, service):
    password = message.text
    passwords[service] = password
    with open(DATA_FILE, "w") as file:
        json.dump(passwords, file)
    bot.reply_to(message, f"Пароль для {service} успішно збережено!")

# отримання пароля
@bot.message_handler(commands=['get'])
def get_password(message):
    msg = bot.reply_to(message, "Введіть назву сервісу:")
    bot.register_next_step_handler(msg, retrieve_password)

def retrieve_password(message):
    service = message.text
    if service in passwords:
        bot.reply_to(message, f"Ваш пароль для {service}: {passwords[service]}")
    else:
        bot.reply_to(message, "Пароль для цього сервісу не знайдено!")

# генерація пароля
@bot.message_handler(commands=['generate'])
def generate_password(message):
    password_length = 12
    characters = string.ascii_letters + string.digits + string.punctuation # масив букв цифр та позначень
    generated_password = ''.join(random.choice(characters) for _ in range(password_length)) # випадковий вибір з масиву(random.choice(characters))
    bot.reply_to(message, f"Ваш новий пароль: {generated_password}")

# запуск бота
print("Бот запущено...")
bot.polling()