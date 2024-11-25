import telebot
import sqlite3
import secrets
import string
from cryptography.fernet import Fernet

TOKEN = "7274151929:AAHkjqiAnVMEL3WMI-FSzGS1nMv4maztn1k"  # Токен від BotFather
bot = telebot.TeleBot(TOKEN)

# Генеруємо ключ шифрування 
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        service TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Привіт! Я бот для управління паролями 🛡️\n"
        "Ось що я вмію:\n"
        "/add - Додати новий пароль\n"
        "/list - Показати всі ваші паролі\n"
        "/generate - Згенерувати новий пароль\n"
    )

# Додавання пароля 
@bot.message_handler(commands=['add'])
def add_password(message):
    bot.reply_to(message, "Напишіть у форматі: *Сервіс Пароль*", parse_mode="Markdown")
    
    @bot.message_handler(func=lambda msg: True)
    def save_password(msg):
        try:
            user_id = msg.from_user.id
            service, password = msg.text.split(" ", 1)
            encrypted_password = cipher.encrypt(password.encode()).decode()

            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords (user_id, service, password) VALUES (?, ?, ?)", 
                           (user_id, service, encrypted_password))
            conn.commit()
            conn.close()

            bot.reply_to(msg, f"Пароль для сервісу '{service}' успішно збережено! ✅")
        except Exception:
            bot.reply_to(msg, "Помилка! Переконайтеся, що ввели дані у правильному форматі.")

# Перегляд паролів
@bot.message_handler(commands=['list'])
def list_passwords(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service, password FROM passwords WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        response = "Ваші паролі:\n"
        for service, encrypted_password in rows:
            password = cipher.decrypt(encrypted_password.encode()).decode()
            response += f"🔐 {service}: {password}\n"
    else:
        response = "У вас немає збережених паролів."

    bot.reply_to(message, response)

# Генерація пароля
@bot.message_handler(commands=['generate'])
def generate_password(message):
    password_length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    generated_password = ''.join(secrets.choice(characters) for _ in range(password_length))
    bot.reply_to(message, f"Ваш новий надійний пароль: `{generated_password}`", parse_mode="Markdown")

# Запуск бота
print("Бот запущено...")
bot.infinity_polling()