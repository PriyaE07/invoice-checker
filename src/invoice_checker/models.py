from decimal import Decimal

from pydantic import BaseModel

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal 