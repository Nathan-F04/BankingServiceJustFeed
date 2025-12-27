"""Banking python file"""

import json
import os
import aio_pika
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from .bankingdb import engine, SessionLocal
from .models import Base, BankUserDB
from .schemas import BankUserCreate, BankUserRead, BankPartialUpdate

app = FastAPI()
Base.metadata.create_all(bind=engine)

#Rabbit MQ
EXCHANGE_NAME = "just_feed_exchange"
RABBIT_URL = os.getenv("RABBIT_URL")

async def get_exchange():
    """
    Open a connection, create a channel and declare a topic exchange.
    Returns (connection, channel, exchange).
    """
    conn = await aio_pika.connect_robust(RABBIT_URL)
    ch = await conn.channel()
    ex = await ch.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC)
    return conn, ch, ex

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
def get_all_bank_cards(db: Session = Depends(get_db)):
    stmt = select(BankUserDB).order_by(BankUserDB.id)
    #Useful for debugging
    result = db.execute(stmt)
    bank_list = result.scalars().all()
    return bank_list

@app.get("/api/banking/{banking_id}", response_model=BankUserRead)
def get_bank_card(banking_id: int, db: Session = Depends(get_db)):
    bank_user = db.get(BankUserDB, banking_id)
    if not bank_user:
        raise HTTPException(status_code=404, detail="bank account not found")
    return bank_user

@app.post("/api/banking", response_model=BankUserRead, status_code=status.HTTP_201_CREATED)
async def add_bank_card(payload: BankUserCreate, db: Session = Depends(get_db)):
    bank_user = BankUserDB(**payload.model_dump())
    db.add(bank_user)
    try:
        db.commit()
        db.refresh(bank_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(e))
    
    #Queue Logic
    conn, ch, ex = await get_exchange()
    msg = aio_pika.Message(body=json.dumps("Card added successfully").encode())
    await ex.publish(msg, routing_key="bank.create")
    await conn.close()
    return bank_user

@app.patch("/api/banking/{banking_id}", response_model=BankUserRead)
async def partial_edit_card(banking_id: int, payload: BankPartialUpdate, db: Session = Depends(get_db)):
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
        #Queue Logic
    conn, ch, ex = await get_exchange()
    msg = aio_pika.Message(body=json.dumps("Card details edited successfully").encode())
    await ex.publish(msg, routing_key="bank.edited")
    await conn.close()
    return updated_user

@app.delete("/api/banking/{banking_id}", status_code=204)
async def delete_bank_card_details(banking_id: int, db: Session = Depends(get_db)) -> Response:
    bank_user = db.get(BankUserDB, banking_id)
    if not bank_user:
        raise HTTPException(status_code=404, detail="Bank user not found")
    db.delete(bank_user)
    db.commit()

    #Queue Logic
    conn, ch, ex = await get_exchange()
    msg = aio_pika.Message(body=json.dumps("Card deleted successfully").encode())
    await ex.publish(msg, routing_key="bank.delete")
    await conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
