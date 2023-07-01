import requests

response = requests.get('http://localhost:3000/fetch-transactions')
transactions = response.json()

for transaction in transactions:
    date = transaction['date']
    direction = transaction['direction']
    amount = transaction['amount']
    print(f"Date: {date}, Direction: {direction}, Amount: {amount}")
