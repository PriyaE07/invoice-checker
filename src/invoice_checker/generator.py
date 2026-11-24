from faker import Faker
from decimal import Decimal
import json
from pathlib import Path
from pydantic import BaseModel

from invoice_checker.models import Vendor
from invoice_checker.models import PurchaseOrder
from invoice_checker.models import POLine

SEED = 42
CATALOG = {
    "Office supplies": {
        "Printer paper, case of 10 reams": Decimal("54.99"),
        "Black toner cartridge": Decimal("89.00"),
        "Ballpoint pens, box of 50": Decimal("12.50"),
        "Sticky notes, pack of 24": Decimal("18.75"),
        "File folders, box of 100": Decimal("21.00"),
    },
    "IT equipment": {
        "Laptop, 14 inch": Decimal("1149.00"),
        "Monitor, 27 inch": Decimal("279.99"),
        "Wireless keyboard": Decimal("49.99"),
        "USB-C docking station": Decimal("189.00"),
        "Ethernet cable, 10 ft": Decimal("8.49"),
    },
    "Medical supplies": {
        "Nitrile gloves, box of 100": Decimal("12.00"),
        "Face masks, box of 50": Decimal("8.00"),
        "Syringes, box of 100": Decimal("24.50"),
        "Gauze pads, pack of 200": Decimal("16.25"),
        "Alcohol prep pads, box of 200": Decimal("6.99"),
    },
    "Cleaning": {
        "Disinfectant spray, case of 12": Decimal("42.00"),
        "Mop heads, pack of 6": Decimal("27.50"),
        "Trash bags, box of 250": Decimal("31.99"),
        "Paper towels, case of 12 rolls": Decimal("38.40"),
        "Hand soap refill, 1 gallon": Decimal("14.95"),
    },
    "Food service": {
        "Coffee beans, 1 kg": Decimal("18.00"),
        "Paper cups, pack of 50": Decimal("6.50"),
        "Bottled water, case of 24": Decimal("5.99"),
        "Sugar packets, box of 1000": Decimal("11.25"),
        "Stir sticks, box of 1000": Decimal("4.75"),
    },
    "Facilities": {
        "LED light bulbs, pack of 12": Decimal("36.00"),
        "HVAC air filter, 20x25": Decimal("15.49"),
        "AA batteries, pack of 48": Decimal("22.99"),
        "Extension cord, 25 ft": Decimal("19.95"),
        "Safety cones, set of 4": Decimal("44.00"),
    },
}


def make_vendor(fake: Faker) -> Vendor:
    return Vendor(
        vendor_name=fake.company(),
        vendor_email=fake.company_email(),
        vendor_phone=fake.phone_number(),
        bank_account_last4=fake.numerify("####"),
        category=fake.random_element(list(CATALOG)),
    )

def make_vendors(fake: Faker, count: int) -> list[Vendor]:
    vendors = []
    for _ in range(count):
        vendors.append(make_vendor(fake))
    return vendors

def make_purchase_order(fake: Faker, vendor: Vendor, po_number: str) -> PurchaseOrder:
    items = CATALOG[vendor.category]
    chosen = fake.random_elements(
        list(items), length=fake.random_int(1, 4), unique=True
    )
    lines = [
        POLine(
            description=name,
            quantity_ordered=fake.random_int(1, 50),
            unit_price=items[name],
        )
        for name in chosen
    ]
    return PurchaseOrder(
        po_number=po_number,
        vendor_name=vendor.vendor_name,
        order_date=fake.date_between(start_date="-90d", end_date="today"),
        lines=lines,
    )

def make_purchase_orders(
    fake: Faker, vendors: list[Vendor], count: int
) -> list[PurchaseOrder]:
    orders = []
    for i in range(count):
        vendor = fake.random_element(vendors)
        orders.append(make_purchase_order(fake, vendor, f"PO-{1001 + i}"))
    return orders


def save_json(items: list[BaseModel], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [item.model_dump(mode="json") for item in items]
    path.write_text(json.dumps(data, indent=2))


def main() -> None:
    Faker.seed(SEED)
    fake = Faker()
    vendors = make_vendors(fake, 10)
    orders = make_purchase_orders(fake, vendors, 20)
    save_json(vendors, Path("data/sample/vendors.json"))
    save_json(orders, Path("data/sample/purchase_orders.json"))
    print(f"Saved {len(vendors)} vendors and {len(orders)} purchase orders to data/sample/")
    