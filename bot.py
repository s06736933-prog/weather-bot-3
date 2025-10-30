import os
import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Инициализация бота
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

# Функция для получения погоды
async def get_weather(city: str) -> str:
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return "❌ API ключ для погоды не настроен"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            return (f"🌤 Погода в Старой Руссе:\n"
                    f"• Температура: {temp:.1f}°C\n"
                    f"• Ощущается как: {feels_like:.1f}°C\n"
                    f"• Влажность: {humidity}%\n"
                    f"• {description.capitalize()}\n"
                    f"• Ветер: {wind_speed} м/с")
        else:
            return "❌ Не удалось получить данные о погоде"
            
    except Exception as e:
        logger.error(f"Ошибка получения погоды: {e}")
        return f"❌ Ошибка при получении погоды: {str(e)}"

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот который может подсказать текущую погоду в городе Старая Русса. Что бы узнать погоду напиши: "погода в Старой Руссе"')

# Обработчик вопроса о погоде
@dp.message()
async def handle_weather_request(message: Message):
    text = message.text.lower()
    
    if "погод" in text and "старой руссе" in text:
        weather_info = await get_weather("Staraya Russa")
        await message.answer(weather_info)
    elif "погод" in text:
        await message.answer('Укажите город, например: "погода в Старой Руссе"')
    else:
        await message.answer('Напишите "погода в Старой Руссе" для получения погоды')

# Запуск бота
async def main():
    logger.info("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())