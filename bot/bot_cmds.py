from aiogram.types import BotCommand

# Список команд бота
private = [
    BotCommand(command='add_note', description='/add_note'),
    BotCommand(command='my_notes', description='/my_notes'),
    BotCommand(command='search_by_tag', description='/search_by_tag'),
    BotCommand(command='edit_note', description='/edit_note'),
    BotCommand(command='delete_note', description='/delete_note'),
]