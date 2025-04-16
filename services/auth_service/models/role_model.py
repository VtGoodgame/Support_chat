from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy import String, create_engine,func ,ForeignKey
from datetime import datetime
from services.consts import DB_URL
from typing import List
import psycopg2

class Base(DeclarativeBase):
    pass

class Roles(Base):
    
  __tablename__ = 'Roles'  # Только имя таблицы
  __table_args__ = {"schema": "support_chat"}  # Схема указывается отдельно
  
  role_id: Mapped[int] = mapped_column(nullable=False,primary_key=True)
  role_name: Mapped[str] = mapped_column(String(50),  nullable=False)
  users = relationship("support_chat.users", back_populates="parent")
  users: Mapped[List["Users"]] = relationship(back_populates="role")
  
# 1. Создаем подключение к БД
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# 2. Создаем таблицы (если их нет)
Base.metadata.create_all(engine)

# 3. Примеры использования сессии
def add_role(role_name: str):
    """Добавление новой роли"""
    session = SessionLocal()
    try:
        new_role = Roles(role_name=role_name)
        session.add(new_role)
        session.commit()
        return new_role.role_id
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении роли: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    try:
        new_id = add_role("User")
        print(f"Добавлена роль c ID {new_id}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")