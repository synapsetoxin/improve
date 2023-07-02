import requests


wallet = 'TPjereztht2j6Ffq3vGyMGwvNvKErVNYuv'
response = requests.get(f"http://localhost:3000/fetch-transactions/{wallet}")
transactions = response.json()


for transaction in transactions:
    date = transaction['date']
    direction = transaction['direction']
    amount = transaction['amount']
    print(f"Date: {date}, Direction: {direction}, Amount: {amount}")

if (response.status_code == 200):
    print("Transactions fetched successfully")

if (len(transactions) == 0):
    print("No transactions found")