"""Validation for Profile Setting Service"""

# app/schemas.py
from typing import Annotated, Optional
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, ConfigDict, StringConstraints

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
Cardstr = Annotated[str, StringConstraints(pattern=r"^\d{16}$")]
pinInt = Annotated[int, Ge(1000), Le(9999)]
balanceInt = Annotated[int, Ge(1)]

# ---------- Banking ----------
class BankUserCreate(BaseModel):
    name: NameStr
    email: EmailStr
    pin: pinInt
    card: Cardstr 
    balance: balanceInt

class BankUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: NameStr
    email: EmailStr
    pin: pinInt
    card: Cardstr
    balance: balanceInt

class BankUserPut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int #Should this be here since we shouldn't be able to edit id?
    name: NameStr
    email: EmailStr
    pin: pinInt
    card: Cardstr
    balance: balanceInt

class BankPartialUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[NameStr] = None
    email: Optional[EmailStr] = None
    pin: Optional[pinInt] = None
    card: Optional[Cardstr] = None
    balance: Optional[balanceInt] = None