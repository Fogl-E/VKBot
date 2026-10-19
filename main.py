from app.template import *
from app.keyboard import *
from app.config import *
from vkbottle.bot import Bot, Message
import logging
import time
from vkbottle import API, GroupEventType, GroupTypes

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.Token)
api = API(token=config.Token)

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
    try:
        user_info = await api.users.get(user_ids=message.from_id)
        user_name = user_info[0].first_name
        await api.messages.send(
            peer_id=config.Admin_id,
            message=f"🔔 Вам сообщение от пользователя! {user_name}",
            random_id=int(time.time())
        )
    except Exception as e:
        print(f"Ошибка при отправке админу: {e}")


@bot.on.message(payload={"cmd":"record"})
async def record(message: Message):
    await message.answer("Записываемся")


@bot.on.message(payload={"cmd":"theme"})
async def theme(message: Message):
    await message.answer("Темы")


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id, 
            message="Спасибо за подписку!", 
            random_id=0
        )
    except Exception as e:
        print(f"Не удалось отправить приветствие: {e}")



bot.run()

