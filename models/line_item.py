from sqlmodel import SQLModel, Field
from typing import Optional, List


class LineItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    status: str
    amount: str
