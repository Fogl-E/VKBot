import datetime

from sqlalchemy import select
from app.keyboard.keyboard import get_free_slots_keyboard, main_keyboard, key_rec
from app.template import *
from app.keyboard import *
from app.config import *
from vkbottle.bot import Bot, Message, MessageEvent
import logging
import time
from vkbottle import API, GroupEventType, GroupTypes
from app.database.connect.connect import con
from app.database.base.database import Appointment, User

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
    await message.answer("Выберите:", keyboard=key_rec)


@bot.on.message(payload={"cmd":"back"})
async def record(message: Message):
    await message.answer("Выберите:", keyboard=main_keyboard)


@bot.on.message(payload={"cmd":"запись"})
async def rec(message: Message):
    for db in con():
        kb_json = get_free_slots_keyboard(db)
        if kb_json is None:
            await message.answer("К сожалению, свободных мест нет.")
            return
    await message.answer("Выберите удобное время:", keyboard=kb_json)


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT)
async def handle_booking(event):
    data = event.get("object", {})
    payload = data.get("payload", {})
    if payload.get("cmd") == "book_slot":
        slot_id = payload.get("slot_id")
        peer_id = data.get("peer_id")
        event_id = data.get("event_id")
        try:
            formatted_time = "Неизвестно"
            for db in con():
                slot = db.query(Appointment).filter(Appointment.id == slot_id).first()
                if not slot:
                    await api.messages.send_message_event_answer(
                        event_id=event_id,
                        user_id=peer_id,
                        peer_id=peer_id,
                        event_data={"type": "show_snackbar", "text": "Упс, это время уже заняли!"}
                    )
                    return
                formatted_time = slot.time_slot.strftime("%d.%m.%Y в %H:%M")
                user = db.query(User).filter(User.id == peer_id).first()
                if not user:
                    user = User(id=peer_id)
                    db.add(user)
                    db.flush()
                user.recording = formatted_time
                db.delete(slot)
                db.commit()
            await api.messages.send_message_event_answer(
                event_id=event_id,
                user_id=peer_id,
                peer_id=peer_id,
                event_data={"type": "show_snackbar", "text": f"Вы записаны на {formatted_time}!"}
            ) 
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")

@bot.on.message(payload={"cmd":"my"})
async def check_my_app(message: Message):
    for db in con():
        user = db.query(User).filter(User.id == message.from_id).first()
        if user and user.recording:
            await message.answer(f"Вы записаны на {user.recording}.")
        else:
            await message.answer("У вас пока нет активных записей.")


@bot.on.message(payload={"cmd":"no"})
async def cancel_app(message: Message):
    for db in con():
        user = db.query(User).filter(User.id == message.from_id).first()
        if user and user.recording:
            try:
                old_time = datetime.datetime.strptime(user.recording, "%d.%m.%Y в %H:%M")
                db.add(Appointment(time_slot=old_time))
            except ValueError:
                pass
            user.recording = None
            db.commit()
            await message.answer("Ваша запись отменена, время снова свободно.")
        else:
            await message.answer("У вас нет активной записи.")


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

