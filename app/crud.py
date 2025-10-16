from sqlalchemy.orm import Session
from sqlalchemy import func, select
from datetime import datetime
from . import models, schemas

# ----- Users -----
def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(name=data.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ----- Categories -----
def create_category(db: Session, data: schemas.CategoryCreate) -> models.Category:
    cat = models.Category(name=data.name, user_id=data.user_id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def list_categories(db: Session, user_id: int):
    return db.scalars(select(models.Category).where(models.Category.user_id == user_id)).all()

# ----- Transactions -----
def create_transaction(db: Session, data: schemas.TransactionCreate) -> models.Transaction:
    txn = models.Transaction(**data.model_dump())
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn

def list_transactions(db: Session, user_id: int):
    return db.scalars(select(models.Transaction).where(models.Transaction.user_id == user_id).order_by(models.Transaction.timestamp.desc())).all()

# ----- Summary -----
def monthly_summary(db: Session, user_id: int, month: str) -> schemas.SummaryOut:
    start = datetime.strptime(month + "-01", "%Y-%m-%d")
    end = start.replace(month=start.month + 1) if start.month < 12 else start.replace(year=start.year + 1, month=1)

    income_total = db.execute(
        select(func.coalesce(func.sum(models.Transaction.amount), 0.0)).where(
            models.Transaction.user_id == user_id,
            models.Transaction.type == "income",
            models.Transaction.timestamp >= start,
            models.Transaction.timestamp < end,
        )
    ).scalar_one()

    expense_total = db.execute(
        select(func.coalesce(func.sum(models.Transaction.amount), 0.0)).where(
            models.Transaction.user_id == user_id,
            models.Transaction.type == "expense",
            models.Transaction.timestamp >= start,
            models.Transaction.timestamp < end,
        )
    ).scalar_one()

    rows = db.execute(
        select(
            models.Transaction.category_id,
            models.Category.name,
            func.coalesce(func.sum(models.Transaction.amount), 0.0),
        )
        .join(models.Category, models.Category.id == models.Transaction.category_id, isouter=True)
        .where(
            models.Transaction.user_id == user_id,
            models.Transaction.type == "expense",
            models.Transaction.timestamp >= start,
            models.Transaction.timestamp < end,
        )
        .group_by(models.Transaction.category_id, models.Category.name)
    ).all()

    by_cat = [
        {"category_id": r[0], "category_name": r[1], "total": float(r[2] or 0.0)}
        for r in rows
    ]

    return schemas.SummaryOut(
        month=month,
        totals=schemas.SummaryTotals(
            income=float(income_total or 0.0),
            expense=float(expense_total or 0.0),
            net=float((income_total or 0.0) - (expense_total or 0.0)),
        ),
        by_category=by_cat,
    )
