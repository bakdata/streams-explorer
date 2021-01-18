#!/usr/bin/env python3

import json

from faker import Faker

fake = Faker()

accounts = []
for i in range(1, 1000):
    account = {
        "account_id": f"a{i}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "country": fake.country(),
    }
    accounts.append(account)

with open("accounts.txt", "w") as f:
    for account in accounts:
        f.write("%s\n" % json.dumps(account))
