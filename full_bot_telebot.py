import telebot
import json
import os

# Получаем токен из переменных окружения Railway
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'data.json'

# Загрузка данных
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Отправь мне своё имя:")

# Обработка сообщений (имя и дополнительные данные)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    user_message = message.text

    data = load_data()

    if user_id not in data:
        data[user_id] = {"name": user_message, "messages": []}
        response = f"Твоё имя сохранено: {user_message}"
    else:
        data[user_id]["messages"].append(user_message)
        response = f"Сообщение добавлено: {user_message}"

    save_data(data)
    bot.reply_to(message, response)

# Запуск бота
bot.polling(none_stop=True)
