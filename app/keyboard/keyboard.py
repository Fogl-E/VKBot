from vkbottle import Keyboard, KeyboardButtonColor, Text

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