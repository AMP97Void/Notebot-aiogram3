from sqlalchemy import BigInteger, Text, DateTime, String, ForeignKey, Integer
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3') # создание бд 

async_session = async_sessionmaker(engine) # Подключение к бд



class Base(AsyncAttrs, DeclarativeBase): #Основной класс, дает возможность управлять всеми дочернеми классами   
    pass

class User(Base):
    __tablename__= 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    userId: Mapped[str] = mapped_column()
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    admintag: Mapped[int] = mapped_column(Integer, default=0)
    
    
class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    
    
class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    text: Mapped[str] = mapped_column(Text)
    
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
            