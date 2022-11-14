import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

bot = Bot('5489514849:AAFZjTao3YlNhpSOk0Q-hXwEE5XclxQwngg')
dp = Dispatcher(bot)

button1 = KeyboardButton('Yeeesss, show it to me!!! ')
button2 = KeyboardButton('No!')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('Yeeesss, show it to me!!!', 'No!')


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}')
    sti = open('C:/not_delete.webp', 'rb')
    await bot.send_sticker(message.chat.id, sti, )
    await message.reply(f'Meowalleykum, {user_full_name}! Do you wanna some kitties?', reply_markup=keyboard)


@dp.message_handler()
async def answer(message: types.Message):
    if message.text == 'No!':
        await bot.send_message(message.chat.id, 'Go away!')
    elif message.text == 'Yeeesss, show it to me!!!':
        await bot.send_message(message.chat.id, 'I`ll show you something')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
