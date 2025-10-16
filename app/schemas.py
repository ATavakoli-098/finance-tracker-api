from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

# ---- Base that enables ORM -> schema (Pydantic v2) ----
class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# ---------------- Users ----------------
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class UserOut(ORMModel):
    id: int
    name: str

# -------------- Categories -------------
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    user_id: int

class CategoryOut(ORMModel):
    id: int
    name: str
    user_id: int

# ------------- Transactions ------------
class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    type: str = Field(pattern=r"^(income|expense)$")
    category_id: Optional[int] = None
    description: Optional[str] = None
    timestamp: datetime

class TransactionOut(ORMModel):
    id: int
    user_id: int
    amount: float
    type: str
    category_id: Optional[int]
    description: Optional[str]
    timestamp: datetime

# ---------------- Summary --------------
class SummaryTotals(BaseModel):
    income: float
    expense: float
    net: float

class SummaryByCategory(BaseModel):
    category_id: Optional[int]
    category_name: Optional[str]
    total: float

class SummaryOut(BaseModel):
    month: str            # YYYY-MM
    totals: SummaryTotals
    by_category: List[SummaryByCategory]
