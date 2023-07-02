import datetime
import json

from dataclasses import dataclass
from typing import List


@dataclass
class Transaction:
    date: datetime
    direction: str
    amount: float


@dataclass
class Transactions(List[Transaction]):

    def load(self, transactions: json) -> None:
        for transaction in transactions:
            date: datetime = transaction['date']
            direction: str = transaction['direction']
            amount: float = transaction['amount']
            self.append(Transaction(date, direction, amount))
