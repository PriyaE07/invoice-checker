from faker import Faker

from invoice_checker.models import Vendor


def make_vendor(fake: Faker) -> Vendor:
    return Vendor(
        vendor_name=fake.company(),
        vendor_email=fake.company_email(),
        vendor_phone=fake.phone_number(),
        bank_account_last4=fake.numerify("####"),
    )

def make_vendors(fake: Faker, count: int) -> list[Vendor]:
    vendors = []
    for _ in range(count):
        vendors.append(make_vendor(fake))
    return vendors