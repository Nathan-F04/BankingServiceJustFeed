"""Banking python file"""

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from .bankingdb import engine, SessionLocal
from .models import Base, BankUserDB
from .schemas import BankUserCreate, BankUserRead, BankPartialUpdate

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def commit_or_rollback(db: Session, error_msg: str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=error_msg)

@app.get("/api/banking", response_model=list[BankUserRead])
def get_all_bank_accounts(db: Session = Depends(get_db)):
    stmt = select(BankUserDB).order_by(BankUserDB.id)
    #Useful for debugging
    result = db.execute(stmt)
    bank_list = result.scalars().all()
    return bank_list
    #return list(db.execute(stmt).scalars())

@app.get("/api/banking/{banking_id}", response_model=BankUserRead)
def get_bank_account(banking_id: int, db: Session = Depends(get_db)):
    bank_user = db.get(BankUserDB, banking_id)
    if not bank_user:
        raise HTTPException(status_code=404, detail="bank account not found")
    return bank_user

@app.post("/api/banking", response_model=BankUserRead, status_code=status.HTTP_201_CREATED)
def add_bank_account(payload: BankUserCreate, db: Session = Depends(get_db)):
    bank_user = BankUserDB(**payload.model_dump())
    db.add(bank_user)
    try:
        db.commit()
        db.refresh(bank_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="bank user already exists")
    return bank_user

@app.put("/api/banking/{banking_id}", response_model=BankUserRead)
def edit_bank_account_details(banking_id: int, payload: BankUserCreate, db: Session = Depends(get_db)):
    bank_user = db.get(BankUserDB, banking_id)
    if not bank_user:
        raise HTTPException(status_code=404, detail="Bank id not found")
    # Update fields from payload
    for key, value in payload.model_dump().items():
        setattr(bank_user, key, value)
    try:
        db.commit()       # ORM knows this is an update
        db.refresh(bank_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Bank user integrity error")

    return bank_user



@app.patch("/api/banking/{banking_id}", response_model=BankUserRead)
def partial_edit_user(banking_id: int, payload: BankPartialUpdate, db: Session = Depends(get_db)):
    # Get only fields that were sent (exclude unset means fields missing from request are ignored)
    edited_bank_details = payload.model_dump(exclude_unset=True)
    
    if not edited_bank_details:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    Bank_account = db.get(BankUserDB, banking_id)
    if not Bank_account:
        raise HTTPException(status_code=404, detail="Bank account id not found")
    try:
        stmt = update(BankUserDB).where(BankUserDB.id == banking_id).values(**edited_bank_details)
        db.execute(stmt)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflict updating user")

    updated_user = db.get(BankUserDB, banking_id)
    return updated_user

@app.delete("/api/banking/{banking_id}", status_code=204)
def delete_bank_account_details(banking_id: int, db: Session = Depends(get_db)) -> Response:
        bank_user = db.get(BankUserDB, banking_id)
        if not bank_user:
            raise HTTPException(status_code=404, detail="Bank user not found")
        #try except here?
        db.delete(bank_user)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
