from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass
class BankUserDB(Base):
    __tablename__ = "banking_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    creditCardNumber: Mapped[str] = mapped_column(String, nullable=False)
    nameOnCard: Mapped[str] = mapped_column(String, nullable=False)
    expMonth: Mapped[int] = mapped_column(Integer, nullable=False)
    expYear: Mapped[int] = mapped_column(Integer, nullable=False)
    cvc: Mapped[int] = mapped_column(Integer, nullable=False)
