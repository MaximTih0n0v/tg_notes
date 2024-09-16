from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем клавиатуру с кнопками на русском языке
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить заметку"),
            KeyboardButton(text="Мои заметки"),
        ],
        [
            KeyboardButton(text="Поиск по тегам"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что Вас интересует?"
)