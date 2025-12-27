"""Validation for Profile Setting Service"""

# app/schemas.py
from typing import Annotated, Optional
from annotated_types import Ge, Le
from pydantic import BaseModel, ConfigDict, StringConstraints

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
Cardstr = Annotated[str, StringConstraints(pattern=r"^\d{16}$")]
yearInt = Annotated[int, Ge(2025), Le(2050)]
monthInt = Annotated[int, Ge(1), Le(12)]
cvcInt = Annotated[int, Ge(100), Le(999)]

# ---------- Banking ----------
class BankUserCreate(BaseModel):
    creditCardNumber: Cardstr
    nameOnCard: NameStr
    expMonth: monthInt
    expYear: yearInt
    cvc: cvcInt

class BankUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    creditCardNumber: Cardstr
    nameOnCard: NameStr
    expMonth: monthInt
    expYear: yearInt
    cvc: cvcInt

class BankPartialUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    creditCardNumber: Optional[Cardstr] = None
    nameOnCard: Optional[NameStr] = None
    expMonth: Optional[monthInt] = None
    expYear: Optional[yearInt] = None
    cvc: Optional[cvcInt] = None