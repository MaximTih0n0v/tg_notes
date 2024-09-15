from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from aiogram import Bot, Dispatcher, types
from sqlalchemy.future import select
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from dotenv import load_dotenv
import logging
from sqlalchemy.orm import sessionmaker
from app.crud import (
    create_note, get_user_by_username, create_user, NoteCreate, get_or_create_tag, get_notes_by_user,
    search_notes_by_tags
)
from app.database import AsyncSessionLocal, DATABASE_URL

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TG_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Dictionary to store user states
user_states = {}

async def send_welcome(message: Message):
    await message.reply("Привет! Я помогу создать заметку. Используйте команду /add_note.")

async def add_note_command(message: Message):
    await message.reply("Введите заголовок заметки:")
    user_states[message.from_user.id] = {"state": "awaiting_title"}

async def handle_message(message: Message, db_session: AsyncSession):
    user_id = message.from_user.id
    username = message.from_user.username

    if user_id in user_states:
        user_state = user_states[user_id]

        if user_state["state"] == "awaiting_title":
            user_state["title"] = message.text
            user_state["state"] = "awaiting_note"
            await message.reply("Введите текст заметки:")

        elif user_state["state"] == "awaiting_note":
            note_text = message.text
            note_title = user_state.get("title", "Без заголовка")

            user = await get_user_by_username(db_session, username)
            if user is None:
                user = await create_user(db_session, username, "default_password")

            user_state["note_title"] = note_title
            user_state["note_text"] = note_text

            user_state["state"] = "awaiting_tags"
            await message.reply("Введите теги для заметки через запятую:")

        elif user_state["state"] == "awaiting_tags":
            tags_text = message.text
            tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]

            note_title = user_state.get("note_title")
            note_text = user_state.get("note_text")

            tag_objects = [await get_or_create_tag(db_session, tag_name) for tag_name in tags]

            user = await get_user_by_username(db_session, username)
            if user:
                try:
                    new_note = await create_note(db_session, note=NoteCreate(title=note_title, content=note_text), user_id=user.id, tags=tag_objects)
                    await message.reply(f"Заметка '{new_note.title}' создана с тегами: {', '.join(tags)}")
                except Exception as e:
                    await message.reply("Произошла ошибка при создании заметки. Попробуйте снова.")
                    logging.error(f"Ошибка создания заметки: {e}")
                    await db_session.rollback()

            del user_states[user_id]

        elif user_state["state"] == "awaiting_tags_for_search":
            tags_text = message.text
            tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]

            try:
                user = await get_user_by_username(db_session, username)
                if user:
                    notes = await search_notes_by_tags(db_session, user.id, tags)
                    if notes:
                        response = "\n\n".join([
                            f"Заметка: {note.title}\n"
                            f"Содержание: {note.content}\n"
                            f"Теги: {', '.join([tag.name for tag in note.tags])}"
                            for note in notes
                        ])
                        await message.reply(f"Найденные заметки по тегам {', '.join(tags)}:\n\n{response}")
                    else:
                        await message.reply(f"Заметки по тегам {', '.join(tags)} не найдены.")
                else:
                    await message.reply("Пользователь не найден.")
            except Exception as e:
                logging.error(f"Ошибка при поиске заметок: {e}")
                await message.reply("Произошла ошибка при поиске заметок. Попробуйте позже.")
            finally:
                del user_states[user_id]
    else:
        await message.reply("Я не понимаю эту команду. Используйте /add_note для создания заметки.")


async def my_notes_command(message: Message, db_session: AsyncSession):
    username = message.from_user.username
    user = await get_user_by_username(db_session, username)

    if user:
        notes = await get_notes_by_user(db_session, user.id)
        if notes:
            # Формируем список с заголовками и содержанием каждой заметки
            note_details = [
                f"Заметка: {note.title}\nСодержание: {note.content}\n" for note in notes
            ]
            response = "\n\n".join(note_details)  # Объединяем все заметки с разделением
            await message.reply(f"Ваши заметки:\n\n{response}")
        else:
            await message.reply("Заметки не найдены.")
    else:
        await message.reply("Пользователь не найден.")

async def search_by_tag_command(message: Message, db_session: AsyncSession):
    logging.info(f"Пользователь {message.from_user.id} начал поиск по тегам.")
    await message.reply("Введите теги для поиска через запятую:")
    user_states[message.from_user.id] = {"state": "awaiting_tags_for_search"}

def with_db_session(handler):
    async def wrapper(message: Message):
        logging.info("Создание сессии базы данных")
        async with AsyncSessionLocal() as db_session:
            try:
                await handler(message, db_session)
            except Exception as e:
                await db_session.rollback()
                logging.error(f"Ошибка работы с базой данных: {e}")
            finally:
                logging.info("Закрытие сессии базы данных")
                await db_session.close()
    return wrapper

async def main():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()

    dp.message.register(send_welcome, Command(commands=["start"]))
    dp.message.register(add_note_command, Command(commands=["add_note"]))
    dp.message.register(with_db_session(my_notes_command), Command(commands=["my_notes"]))
    dp.message.register(with_db_session(search_by_tag_command), Command(commands=["search_by_tag"]))

    # Регистрируем только одну функцию для текстовых сообщений
    dp.message.register(with_db_session(handle_message))

    logging.info("Бот запускается...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка во время запуска бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
