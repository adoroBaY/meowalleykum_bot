import logging
import requests
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command

API_TOKEN = '5489514849:AAH2BMUFj7oU_Hp8uNoi5QxzgK2skIPSbD8'
CAT_API_URL = "https://api.thecatapi.com/v1/images/search?format=json"  # The Cat API URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Настройка клавиатуры
button1 = KeyboardButton(text='Yeeesss!!!')
button2 = KeyboardButton(text='No!')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button1, button2]])

# Проверка подключения к The Cat API
def test_cat_api():
    try:
        response = requests.get(CAT_API_URL)
        response.raise_for_status()
        data = response.json()
        image_url = data[0]["url"]
        logging.info(f"Test API Connection: Image URL received: {image_url}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Test API Connection failed: {e}")
        return False

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}')
    
    try:
        with open('not_delete.webp', 'rb') as sti:
            await bot.send_sticker(message.chat.id, sti)
    except FileNotFoundError:
        await message.reply(
            f'Meowalleykum, {user_full_name}! Do you wanna some kitties?', 
            reply_markup=keyboard
        )
        return

    await message.reply(
        f'Meowalleykum, {user_full_name}! Do you wanna some kitties?', 
        reply_markup=keyboard
    )

# Обработчик сообщений от пользователя
@dp.message()
async def answer(message: types.Message):
    if message.text == 'No!':
        await bot.send_message(message.chat.id, 'Go away!')
        try:
            with open('brother.jpg', 'rb') as bro:
                await bot.send_photo(message.chat.id, bro.read())
        except FileNotFoundError:
            await bot.send_message(message.chat.id, "Brother image not found.")

    elif message.text == 'Yeeesss!!!':
        await bot.send_message(message.chat.id, 'I`ll show you something')

        try:
            response = requests.get(CAT_API_URL)
            response.raise_for_status()
            data = response.json()
            image_url = data[0]["url"]
            logging.info(f"Received image URL: {image_url}")

            # Скачиваем изображение
            image_data = requests.get(image_url).content
            image_path = os.path.join(os.getcwd(), "cat.jpg")
            with open(image_path, "wb") as f:
                f.write(image_data)
            logging.info(f"Image saved successfully to {image_path}.")

            # Отправляем изображение котика
            with open(image_path, 'rb') as cat_image:
                await bot.send_photo(chat_id=message.chat.id, photo=cat_image)
            logging.info("Image sent successfully.")

            await bot.send_message(message.chat.id, text="Do you want more kitties?")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            await bot.send_message(message.chat.id, text=f"Error fetching cat image: {e}")
        except (KeyError, IndexError):
            logging.error("Error processing API response.")
            await bot.send_message(message.chat.id, text="Error processing cat API response.")
        except FileNotFoundError:
            logging.error("File cat.jpg not found.")
            await bot.send_message(message.chat.id, 'Cat image not found.')

    elif message.text == 'MORE!':
        try:
            image_path = os.path.join(os.getcwd(), "cat.jpg")
            with open(image_path, 'rb') as cat_image:
                await bot.send_photo(chat_id=message.chat.id, photo=cat_image)
            logging.info("Resending previously saved image.")
        except FileNotFoundError:
            logging.error("File cat.jpg not found.")
            await bot.send_message(message.chat.id, 'Cat image not found.')

# Основная функция для запуска бота
async def main():
    logging.basicConfig(level=logging.INFO)

    # Проверка API перед запуском
    if not test_cat_api():
        logging.error("The Cat API is not reachable. Exiting.")
        return

    await dp.start_polling(bot)

# Точка входа в приложение
if __name__ == '__main__':
    asyncio.run(main())
