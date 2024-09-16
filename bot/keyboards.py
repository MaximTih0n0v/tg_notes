from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем клавиатуру с кнопками на русском языке
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/add_note"),
            KeyboardButton(text="/my_notes"),
        ],
        [
            KeyboardButton(text="/search_by_tag"),
        ],
        [
            KeyboardButton(text="/edit_note"),
        ],
        [
            KeyboardButton(text="/delete_note"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Работаем с заметками ..."
)