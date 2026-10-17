from app.template import *
from app.keyboard import *
from app.config import *
from vkbottle.bot import Bot, Message
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.Token)


@bot.on.message(text="старт")
async def start(message: Message):
    await message.answer("Выберите раздел:", keyboard=main_keyboard)


@bot.on.message(payload={"cmd":"about"})
async def about(message: Message):
    await message.answer("Обо мне")


@bot.on.message(payload={"cmd":"coast"})
async def coast(message: Message):
    await message.answer("воть", template=my_temp)


@bot.on.message(payload={"cmd":"vik"})
async def vik(message: Message):
    await message.answer("я пошёл, ждём викторию")


@bot.on.message(payload={"cmd":"record"})
async def record(message: Message):
    await message.answer("Записываемся")


@bot.on.message(payload={"cmd":"theme"})
async def theme(message: Message):
    await message.answer("Темы")


bot.run()

