import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

API_KEY = '793254d4affeda81ec9713f9fe23dbba'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text('Привет! Напиши название города, чтобы узнать погоду.')

def get_weather(city: str) -> str:
  url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
  response = requests.get(url)
  data = response.json()

  if response.status_code != 200:
    return 'Ошибка при получении данных о погоде. Пожалуйста, попробуйте снова.'

  if data['cod'] != 200:
    return 'Город не найден.'

  temperature = data['main']['temp']
  weather_description = data['weather'][0]['main'] # Изменено!
  wind_speed = data['wind']['speed']
  clouds = data['clouds']['all']

  return f'Температура: {temperature}°C\nОсадки: {weather_description}\nСкорость ветра: {wind_speed} м/с\nОблачность: {clouds}%'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  city = update.message.text
  weather_info = get_weather(city)
  await update.message.reply_text(weather_info)

def main() -> None:
  application = ApplicationBuilder().token('8126486909:AAGZMo6r11MNt3boAmHVFr_-xAoAqQGhyeE').build()

  application.add_handler(CommandHandler('start', start))
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

  application.run_polling()

if __name__ == '__main__': # Исправлено!
  main()
