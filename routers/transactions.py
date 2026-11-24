import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/transactions", tags=["Transactions"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get(path="/", response_model=list[TransactionRead])
async def get_transactions(session: SessionDepend):
    try:
        result = await session.execute(select(Transaction))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get transactions")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transactions",
        ) from exc


@router.get(path="/{transaction_id}", response_model=TransactionRead)
async def get_transaction(transaction_id: int, session: SessionDepend):
    try:
        result = await session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        transaction = result.scalars().first()
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
            )
        return transaction
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get transaction with id %d", transaction_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transaction",
        ) from exc


@router.post(
    path="/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction_data: TransactionCreate, session: SessionDepend
):
    try:
        new_transaction = Transaction(**transaction_data.model_dump())
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
        return new_transaction
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create transaction")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction",
        ) from exc


@router.put(path="/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    session: SessionDepend,
):
    try:
        result = await session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        existing_transaction = result.scalars().first()
        if not existing_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
            )

        for field, value in transaction_update.model_dump(exclude_unset=True).items():
            setattr(existing_transaction, field, value)

        session.add(existing_transaction)
        await session.commit()
        await session.refresh(existing_transaction)
        return existing_transaction
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update transaction with id %s", transaction_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update transaction",
        ) from exc


@router.delete(path="/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: SessionDepend):
    try:
        result = await session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        existing_transaction = result.scalars().first()
        if not existing_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
            )

        await session.delete(existing_transaction)
        await session.commit()
        return None
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete transaction with id %s", transaction_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete transaction",
        ) from exc
