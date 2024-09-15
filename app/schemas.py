from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Схема для тегов
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

# Схема для заметок
class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[TagBase]] = []

# Схема для создания заметки
class NoteCreate(NoteBase):
    pass

# Схема для обновления заметки
class NoteUpdate(NoteBase):
    pass

# Схема для отображения заметки
class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схема для пользователя
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
