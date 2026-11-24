from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr


class LineItem(BaseModel):
    description: str
    quantity: int = Field(gt=0)
    unit_price: Decimal
    line_total: Decimal


class Invoice(BaseModel):
    invoice_number: str = Field(
        description=(
            "The vendor's invoice number, often labeled 'Invoice #' or 'Inv No.'. "
            "Not the PO number, customer number, or account number."
        )
    )
    vendor_name: str = Field(
        description=(
            "The company that sent the invoice and is asking to be paid. "
            "Not the 'Bill To' or 'Ship To' company."
        )
    )
    invoice_date: date = Field(
        description=(
            "The date the invoice was issued, not the due date or delivery date. "
            "Read the date using the vendor's country format, "
            "then always return it as YYYY-MM-DD."
        )
    )
    po_number: str | None = Field(
        default=None,
        description="The purchase order number the invoice refers to. Null if not shown.",
    )
    payment_terms: str | None = None
    line_items: list[LineItem] = Field(min_length=1)
    subtotal: Decimal | None = None
    tax: Decimal | None = None
    total: Decimal = Field(
        description=(
            "The final amount due, including tax and fees. "
            "Not the subtotal or any balance carried from earlier invoices."
        )
    )
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")


class POLine(BaseModel):
    description: str
    quantity_ordered: int = Field(gt=0)
    unit_price: Decimal
    quantity_billed: int = Field(default=0, ge=0)


class PurchaseOrder(BaseModel):
    po_number: str
    vendor_name: str
    order_date: date
    lines: list[POLine] = Field(min_length=1)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")


class Vendor(BaseModel):
    vendor_name: str
    vendor_email: EmailStr
    bank_account_last4: str = Field(pattern=r"^\d{4}$")
    vendor_phone: str