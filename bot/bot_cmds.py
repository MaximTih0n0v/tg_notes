from aiogram.types import BotCommand

# Список команд бота
private = [
    BotCommand(command='add_note', description='Добавить заметку'),
    BotCommand(command='my_notes', description='Мои заметки'),
    BotCommand(command='search_by_tag', description='Поиск по тегам'),
]