from app.database.models import async_session
from datetime import datetime
from app.database.models import User, Category, Note


from sqlalchemy import select, update
from sqlalchemy import delete as sa_delete



async def set_user(tg_id: int, name: str, userId: str, data: datetime):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             name=name,
                             userId=userId))
            await session.commit()
            return True  # пользователь был добавлен
        return False  # пользователь уже есть
            
# Добавление категории, с проверкой на существование
async def new_category(name: str):
    async with async_session() as session:
        existing_category = await session.scalar(
            select(Category).where(Category.name == name)
        )

        if existing_category:
            return False  # категория уже есть

        session.add(Category(name=name))
        await session.commit()
        return True  # успешно добавлено
    
    
async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()  # вернёт список строк
    
    
async def get_my_notes(user_id: int):
    async with async_session() as session:
    
        result = await session.execute(select(Note).where(Note.user_id == user_id))
        return result.scalars().all()  # вернёт список строк


async def create_note(user_id: int, name: str, text: str, category: int = 1):
    async with async_session() as session:
        new_note = Note(
            user_id=user_id,
            name=name,
            text=text,
            category=category
        )
        session.add(new_note)
        await session.commit()
        
async def giveapanel(tg_id: int, adminTag: int):
    async with async_session() as session:
        admin = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not admin: 
            return False
        
        admin.admintag = adminTag  # меняем поле у найденного пользователя
        await session.commit()
        return True
        
async def chekAdmin(tg_id: int):
    async with async_session() as session:
        chek = await session.scalar(select(User.admintag).where(User.tg_id == tg_id))
        
        if chek == 1:
            return True
        else:
            return False
        
async def changeNoteName(id:int, name: str, userId: int):
    async with async_session() as session:
        find =   await session.execute(
            update(Note).where(Note.id == id, Note.user_id == userId).values(name=name)
        )
        
        if find.rowcount == 0:
            return False  # ничего не обновилось (записи с таким id нет)
        
        await session.commit()
        return True
    
async def changeNoteText(id:int, ntext: str, userId: int):
    async with async_session() as session:
        find =   await session.execute(
            update(Note).where(Note.id == id, Note.user_id == userId).values(text=ntext)
        )
        
        if find.rowcount == 0:
            return False  # ничего не обновилось (записи с таким id нет)
        
        await session.commit()
        return True
    
    
async def clearAll(id: int):
    async with async_session() as session:
        clear = sa_delete(Note).where(Note.user_id == id)
        result = await session.execute(clear)
        await session.commit()

        # Получить количество удалённых строк:
        if result.rowcount == 0:
            print("Ничего не удалено")
            return False
        else:
            print(f"Удалено {result.rowcount} записей")
            return True
        
async def delete(userId: int, noteId: int):
    async with async_session() as session:
        stmt = select(Note).where(Note.id == noteId, Note.user_id == userId)
        result = await session.execute(stmt)
        note = result.scalar_one_or_none()
  
        if note:
            await session.delete(note)
            await session.commit()
            return True
        else:
            return False
        
async def clearall():
    async with async_session() as session:
        clear = sa_delete(Note)
        result = await session.execute(clear)
        await session.commit()

        # Получить количество удалённых строк:
        count = result.rowcount
        if count is None or count == 0:
            print("Ничего не удалено")
            return False
        else:
            print(f"Удалено {count} записей")
            return True