import asyncio
import json
import random
from datetime import datetime

categories = ["Mercedes", "Porshe", "BMW", "Lamborgini", "Mazda",
              "Toyota", "Lada", "Subaru", "Jaguar", "Lexus"]


def generate_transaction():
    return {
        "timestamp": datetime.now().isoformat(),
        "category": random.choice(categories),
        "amount": round(random.uniform(10.0, 1000.0), 2),
    }


async def generate_transactions(num_transactions):
    transactions = []
    batch_number = 1

    for i in range(num_transactions):
        transactions.append(generate_transaction())

        if len(transactions) == 10 or i == num_transactions - 1:
            save_to_file(transactions, )
            print(f"Batch {batch_number}"
                  f" saved with {len(transactions)} transactions.")
            transactions.clear()
            batch_number += 1

        await asyncio.sleep(0.1)


def save_to_file(transactions, batch_number):
    filename = f"transactions_batch_{batch_number}.json"
    with open(filename, mode="w") as file:
        file.write(json.dumps(transactions, indent=4))


async def process_transactions(file_name):
    with open(file_name, "r") as file:
        transactions = json.load(file)

    category_totals = {}
    for transaction in transactions:
        category = transaction["category"]
        amount = transaction["amount"]
        category_totals[category] = category_totals.get(category, 0) + amount

    return category_totals


async def process_all_batches(batch_count):
    aggregated_totals = {}

    for batch_number in range(1, batch_count + 1):
        file_name = f"transactions_batch_{batch_number}.json"
        try:
            print(f"Processing file: {file_name}")
            batch_totals = await process_transactions(file_name)
            for category, total in batch_totals.items():
                aggregated_totals[category] = aggregated_totals.get(category,
                                                                    0) + total
        except FileNotFoundError:
            print(f"File {file_name} not found. Skipping.")

    spending_limit = 2000
    for category, total in aggregated_totals.items():
        print(f"Category: {category}, Total Amount: {total}")
        if total > spending_limit:
            print(f"ALERT: Spending limit exceeded in category '{category}'!"
                  f" Total: {total}")


async def main():
    num_transactions = int(input("Enter the number"
                                 "of transactions to generate: "))

    await generate_transactions(num_transactions)

    batch_count = (num_transactions + 9) // 10
    await process_all_batches(batch_count)

if __name__ == "__main__":
    asyncio.run(main())
