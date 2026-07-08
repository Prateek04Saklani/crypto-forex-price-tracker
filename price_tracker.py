import requests

from datetime import datetime, UTC

print("Crypto & Forex Market Tracker")
print("-----------------------------\n")

crypto_input = input("Enter Crypto symbols (comma seperated or press Enter for default): ")
if not crypto_input.strip():
    crypto_ids = ['bitcoin', 'ethereum', 'solana', 'binancecoin', 'ripple']
else:
    crypto_ids = [c.strip().lower() for c in crypto_input.split(',')]


forex_input = input("Enter Forex pairs (comma sperated or press Enter for default): ")
if not forex_input.strip():
    forex_pairs = ['USD/EUR', 'USD/JPY', 'USD/CHF', 'GBP/USD', 'AUD/USD']
else:
    forex_pairs = [p.strip().upper() for p in forex_input.split(',')]


print("\nFetching market data...\n")

print("CryptoCurrencies Prices")
print("-" * 80)
print(f"{'Coin':<10} {'Price':<15} {'24h Change':<13} {'Market Cap':<15} {'Volume (24)'}")
print("-" * 80)


url = f"https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency' : 'usd',
    'ids': ','.join(crypto_ids),
    'order': 'market_cap_desc'

}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    crypto_data = response.json()

    for coin in crypto_data:
        symbol = coin['symbol'].upper()
        price = coin['current_price']
        change_24h = coin['price_change_percentage_24h']
        market_cap = coin['market_cap']
        volume = coin['total_volume']

        price_str = f"${price:,.2f}" if price >= 1 else f"${price:.4f}"
        change_str = f"{'+' if change_24h >= 0 else ''}{change_24h:.2f}%"

        print(f"{symbol:<10} {price_str:<15} {change_str:<13} ${market_cap:,.0f}    ${volume:,.0f}")

except Exception as e:
    print(f"Error in fetching crypto data: {e}")

print("-" * 80)
print()

print("FOREX EXCHANGE RATES")
print("-" * 80)
print(f"{'Pair':<15} {'Rate':<12} {'Change':<12} {'Spread'}")
print("-" * 80)

base_url = "https://api.exchangerate-api.com/v4/latest/"

forex_results = []

for pair in forex_pairs:
    parts = pair.split('/')
    if len(parts) != 2:
        continue


    base, target = parts


    try:
        response = requests.get(f"{base_url}{base}")
        data = response.json()


        if target in data['rates']:
            rate = data['rates'][target]

            change_percent = 0 

            spread = rate * 0.0002

            forex_results.append({
                'pair': pair,
                'rate': rate,
                'change': change_percent,
                'spread': spread
            })
    
    except:
        continue


for result in forex_results:
    rate_str = f"{result['rate']:.4f}"
    change_str = f"{'+' if result['change'] >= 0 else ''}{result['change']:.2f}%"
    spread_str = f"{result['spread']:.4f}"

    print(f"{result['pair']:<15} {rate_str:<12} {change_str:<12} {spread_str}")


print("-" * 80)
print()


now = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
print(f"Last Updated: {now} UTC")
print("Market Status: 24/7 Trading Active")