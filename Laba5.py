import telebot
from cryptography.fernet import Fernet
import json

# Генеруємо ключ для шифрування (збережіть цей ключ у безпечному місці!)
# Використовуйте його, щоб створити об'єкт шифрування.
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Створіть файл для збереження паролів
DATA_FILE = "passwords.json"

# Завантаження або створення бази даних паролів
try:
    with open(DATA_FILE, "r") as file:
        passwords = json.load(file)
except FileNotFoundError:
    passwords = {}

# Ініціалізація бота
API_TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(API_TOKEN)

# Команда старт
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привіт! Я бот для управління паролями. Використовуйте команди:\n"
                          "/add - додати новий пароль\n"
                          "/get - отримати пароль\n"
                          "/generate - згенерувати надійний пароль")

# Додати новий пароль
@bot.message_handler(commands=['add'])
def add_password(message):
    msg = bot.reply_to(message, "Введіть назву сервісу:")
    bot.register_next_step_handler(msg, get_service_name)

def get_service_name(message):
    service = message.text
    msg = bot.reply_to(message, "Введіть ваш пароль:")
    bot.register_next_step_handler(msg, lambda m: save_password(m, service))

def save_password(message, service):
    password = message.text
    encrypted_password = cipher.encrypt(password.encode()).decode()
    passwords[service] = encrypted_password
    with open(DATA_FILE, "w") as file:
        json.dump(passwords, file)
    bot.reply_to(message, f"Пароль для {service} успішно збережено!")

# Отримати збережений пароль
@bot.message_handler(commands=['get'])
def get_password(message):
    msg = bot.reply_to(message, "Введіть назву сервісу:")
    bot.register_next_step_handler(msg, retrieve_password)

def retrieve_password(message):
    service = message.text
    if service in passwords:
        encrypted_password = passwords[service]
        password = cipher.decrypt(encrypted_password.encode()).decode()
        bot.reply_to(message, f"Ваш пароль для {service}: {password}")
    else:
        bot.reply_to(message, "Пароль для цього сервісу не знайдено!")

# Згенерувати надійний пароль
import random
import string

@bot.message_handler(commands=['generate'])
def generate_password(message):
    password_length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    generated_password = ''.join(random.choice(characters) for _ in range(password_length))
    bot.reply_to(message, f"Ваш новий пароль: {generated_password}")

# Запуск бота
bot.polling()
