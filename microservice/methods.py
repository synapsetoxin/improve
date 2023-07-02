import requests
import json

from typing import Optional

from app.src.database.models import Wallet


def fetch(wallet: Wallet) -> Optional[json]:
    response = requests.get(f"http://localhost:3000/fetch-transactions/{wallet.address}")
    transactions = response.json()
    if response.status_code == 200 and len(transactions):
        return transactions
    return None
