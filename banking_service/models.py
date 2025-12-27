from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass
class BankUserDB(Base):
    __tablename__ = "banking_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer) #make this a foreign key
    card_number: Mapped[str] = mapped_column(String, nullable=False)
    name_on_card: Mapped[str] = mapped_column(String, nullable=False)
    month_of_expiry: Mapped[int] = mapped_column(Integer, nullable=False)
    year_of_expiry: Mapped[int] = mapped_column(Integer, nullable=False)
    cvc: Mapped[int] = mapped_column(Integer, nullable=False)
