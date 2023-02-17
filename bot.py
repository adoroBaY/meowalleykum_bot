import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

API_TOKEN = '5489514849:AAH2BMUFj7oU_Hp8uNoi5QxzgK2skIPSbD8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
button1 = KeyboardButton('Yeeesss!!!')
button2 = KeyboardButton('No!')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button1, button2]])


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}')
    sti = open('/not_delete.webp', 'rb')
    await bot.send_sticker(message.chat.id, sti, )
    await message.reply(f'Meowalleykum, {user_full_name}! Do you wanna some kitties?', reply_markup=keyboard)


@dp.message_handler()
async def answer(message: types.Message):
    if message.text == 'No!':
        await bot.send_message(message.chat.id, 'Go away!')
        with open('/brother.jpg', 'rb') as bro:
            bro = bro.read()
            await bot.send_photo(message.chat.id, bro)
    elif message.text == 'Yeeesss!!!':
        await bot.send_message(message.chat.id, 'I`ll show you something')

        response = requests.get("https://api.thecatapi.com/v1/images/search?format=json")
        data = response.json()
        image_url = data[0]["url"]

        with open("cat.jpg", "wb") as f:
            f.write(requests.get(image_url).content)

            await bot.send_photo(chat_id=message.chat.id, photo=open('cat.jpg', 'rb'))
            await bot.send_message(chat_id=message.chat.id, text="Do you want more kitties?")

            if message.text == 'MORE!':
                await bot.send_message(message.chat.id, 'Ok!')
                await bot.send_photo(chat_id=message.chat.id, photo=open('cat.jpg', 'rb'))

if __name__ == '__app__':
    executor.start_polling(dp, skip_updates=True)

