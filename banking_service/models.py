from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class UserDB(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)

class BankUserDB(Base):
    __tablename__ = "banking_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    creditCardNumber: Mapped[str] = mapped_column(String, nullable=False)
    nameOnCard: Mapped[str] = mapped_column(String, nullable=False)
    expMonth: Mapped[int] = mapped_column(Integer, nullable=False)
    expYear: Mapped[int] = mapped_column(Integer, nullable=False)
    cvc: Mapped[int] = mapped_column(Integer, nullable=False)
