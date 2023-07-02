import requests

from typing import Optional

from app.src.database.models import Wallet
from microservice.models import Transactions


def fetch(wallet: Wallet) -> Optional[Transactions]:
    response = requests.get(f"http://localhost:3000/fetch-transactions/{wallet.address}")
    transactions = Transactions()
    transactions.load(response.json())
    if response.status_code == 200 and len(transactions):
        return transactions
    return None
