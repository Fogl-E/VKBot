from vkbottle import Callback, Keyboard, KeyboardButtonColor, Text
from app.database.base.database import Appointment
import datetime

main_keyboard=(
    Keyboard(one_time=False)
    .add(Text("🧠Обо мне", {"cmd":"about"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("🧘‍♀️ Темы: психология", {"cmd":"theme"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("📝 Запись", {"cmd":"record"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("💰 Стоимость", {"cmd":"coast"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("🙋‍♀️✨ Обратиться к Виктории", {"cmd":"vik"}), color=KeyboardButtonColor.PRIMARY)
)

def get_free_slots_keyboard(db) -> str | None:
    keyboard = Keyboard(inline=True)
    free_slots = db.query(Appointment).filter(
        Appointment.time_slot > datetime.datetime.now()
    ).all()
    if not free_slots:
        return None 
    for i, slot in enumerate(free_slots):
        time_str = slot.time_slot.strftime("%d %b, %H:%M")
        keyboard.add(
            Callback(label=time_str, payload={"cmd": "book_slot", "slot_id": slot.id, "time": str(slot.time_slot)})
        )
        if (i + 1) % 2 == 0: keyboard.row()
        
    return keyboard.get_json()

key_rec=(
    Keyboard(one_time=False)
    .add(Text("📝 Записаться", {"cmd":"запись"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("🧘‍♀️ Отменить занятие", {"cmd":"no"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("📝 Моя запись", {"cmd":"my"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Назад", {"cmd":"back"}), color=KeyboardButtonColor.PRIMARY)
)