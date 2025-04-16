from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column , Session, sessionmaker, relationship
from sqlalchemy import String, ForeignKey, select, update, delete,func, create_engine
from datetime import datetime
import services.consts as consts
import psycopg2
from services.auth_service.models.role_model import Roles 


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "support_chat.users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_role: Mapped[int] =  mapped_column(ForeignKey('support_chat.Roles.role_id'), default=1)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    role: Mapped["Roles"] = relationship(back_populates="users")
 
 
engine = create_engine(consts.DB_URL)
SessionLocal = sessionmaker(bind=engine)
    
Base.metadata.create_all(engine, tables=[
    Roles.__table__,
    Users.__table__
])
    
def add_user(
    username: str, 
    email: str, 
    password_hash: str,
    id_role: int = 1,  # default value
    phone_number: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    created_at: Optional[datetime] = None,
    is_active: bool = False
):
    """Добавление нового пользователя"""
    Session = SessionLocal()
    try:
        new_user = Users(
            id_role= 2,
            username=username,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            created_at=created_at or datetime.now(),  # если не передано, используем текущее время
            is_active=is_active,
            last_login=datetime.now()  # всегда текущее время при создании
        )
        Session.add(new_user)
        Session.commit()
        return new_user.id
    except Exception as e:
        Session.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")
        raise
    finally:
        Session.close()

if __name__=="__main__":
    try:
        new_user = add_user(  
            username="vtgoodgame",
            email="devisheva.ina@gmail.com",
            password_hash="password")
        
        print(f"Добавлен новый пользователь с ID {new_user}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    
