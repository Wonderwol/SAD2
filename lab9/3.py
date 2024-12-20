def calculate_shipping(country, weight):
    rates = {
        "USA": [10, 20],
        "Canada": [15, 25]
    }

    default_rate = [30, 50]

    rate = rates.get(country, default_rate)

    return rate[0] if weight < 5 else rate[1]
