def calculate_total(order):
    total = 0
    for item in order["items"]:
        total += item["price"] * item["quantity"]
    return total


def process_payment():
    print("Processing payment...")
    print("Payment successful!")


def send_confirmation_email():
    print("Sending confirmation email...")


def complete_order():
    print("Order complete.")


def process_order(order):
    total = calculate_total(order)
    print(f"Total: {total}")
    process_payment()
    send_confirmation_email()
    complete_order()
