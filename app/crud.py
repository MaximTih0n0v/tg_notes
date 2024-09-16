from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from .models import Note, Tag, User
from .schemas import NoteCreate
from sqlalchemy.orm import selectinload
import logging
from .models import note_tags  # Импортируем промежуточную таблицу

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def create_note(db_session: AsyncSession, note: NoteCreate, user_id: int, tags: list[Tag]):
    new_note = Note(title=note.title, content=note.content, user_id=user_id, tags=tags)
    db_session.add(new_note)
    try:
        await db_session.commit()
        await db_session.refresh(new_note)
    except Exception as e:
        await db_session.rollback()  # Откатываем изменения при ошибке
        logging.error(f"Ошибка создания заметки: {e}")
        raise
    return new_note


async def search_notes_by_tags(db_session: AsyncSession, user_id: int, tags: list[str]):
    logging.info(f"Поиск заметок для пользователя {user_id} с тегами: {tags}")

    # Логирование до запроса
    logging.info("Выполняем запрос на поиск тегов")
    result = await db_session.execute(select(Tag).filter(Tag.name.in_(tags)))

    found_tags = result.scalars().all()

    if not found_tags:
        logging.info(f"Теги не найдены: {tags}")
        return []

    tag_ids = [tag.id for tag in found_tags]
    logging.info(f"Найдены теги с ID: {tag_ids}")

    result = await db_session.execute(
        select(Note)
        .join(note_tags)
        .filter(note_tags.c.tag_id.in_(tag_ids), Note.user_id == user_id)  # Фильтруем по user_id
        .options(selectinload(Note.tags))
        .distinct()
    )
    notes = result.scalars().all()

    logging.info(f"Найдено заметок: {len(notes)}")
    return notes



async def get_user_by_username(db_session: AsyncSession, username: str):
    result = await db_session.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db_session: AsyncSession, username: str, password: str):
    new_user = User(username=username, password=password)
    db_session.add(new_user)
    try:
        await db_session.commit()
        await db_session.refresh(new_user)
    except Exception as e:
        await db_session.rollback()  # Откатываем изменения при ошибке
        logging.error(f"Ошибка создания пользователя: {e}")
        raise
    return new_user


async def get_or_create_tag(db_session: AsyncSession, tag_name: str):
    result = await db_session.execute(select(Tag).filter(Tag.name == tag_name))
    tag = result.scalars().first()

    if not tag:
        tag = Tag(name=tag_name)
        db_session.add(tag)
        try:
            await db_session.commit()
            await db_session.refresh(tag)
        except Exception as e:
            await db_session.rollback()  # Откатываем изменения при ошибке
            logging.error(f"Ошибка создания тега: {e}")
            raise
    return tag


async def get_notes_by_user(db_session: AsyncSession, user_id: int):
    result = await db_session.execute(select(Note).filter(Note.user_id == user_id))
    return result.scalars().all()

async def get_note_by_id(db_session: AsyncSession, note_id: int):
    result = await db_session.execute(select(Note).filter(Note.id == note_id))
    return result.scalars().first()

async def update_note(db_session: AsyncSession, note_id: int, new_title: str, new_content: str):
    result = await db_session.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()

    if note:
        note.title = new_title
        note.content = new_content
        try:
            await db_session.commit()
            await db_session.refresh(note)
        except Exception as e:
            await db_session.rollback()
            logging.error(f"Ошибка обновления заметки: {e}")
            raise
    return note
