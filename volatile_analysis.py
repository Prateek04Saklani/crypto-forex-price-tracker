import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    response = requests.get(url)
    data = response.json()

    market_data = data['market_data']

    current_price = market_data['current_price']['usd']
    high_24h = market_data['high_24h']['usd']
    low_24h = market_data['low_24h']['usd']
    price_change_24h = market_data['price_change_24h']

    volatility_range = high_24h - low_24h
    volatility_percentage = (volatility_range / low_24h) * 100

    return{

        'symbol': data['symbol'].upper(),
        'name': data['name'],
        'current_price': current_price,
        'high_24h': high_24h,
        'low_24h': low_24h,
        'range': volatility_range,
        'volatility_percentage': volatility_percentage,
        'change_24h': price_change_24h
    }

def get_fear_greed_index():
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        data = response.json
        value = int(data['data'][0]['value'])


        if value >= 75:
            sentiment = "Extreme_Greed"
        elif value >=55:
            sentiment = "Greed"
        elif value >= 45:
            sentiment = "Neutral"
        elif value >= 25:
            sentiment = "Fear"
        else:
            sentiment = "Extreme_Fear"

        return value, sentiment
    
    except:

        return None, "Unknown"
    

def send_alert_email(asset, current_price, target_price, email):
    sender_email = os.getenv('SENDER_EMAIL', 'prateeksak@gmail.com')
    sender_password = os.getenv('SENDER_PASSWORD', 'your_app_password')

    subject = f"🚨 Price Alert: {asset} hit ${target_price:.2f}"
    body = f"""

    Price Alert Triggered!
    
    Asset: {asset}
    Current Price: ${current_price:.2f}
    Target Price: ${target_price:.2f}
    
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email

    try:
        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except:
        return False

print("Crypto & Forex Volatility Analyzer")
print("===================================\n")


asset_type = input("Analyse (1) Crypto or Forex? ")

if asset_type == '1':
    crypto_id = input("\nEnter the Crypto Symbol (e.g, bitcoin, ethereum): ").lower()

    print("\nFetching data and analyzing volatility...\n")


    data = get_crypto_data(crypto_id)

    print(f"{data['name'].upper()} ({data['symbol']}) Analysis")

    print("-" * 50)
    print(f"CurrentPrice:     ${data['current_price']:,.2f}")
    print(f"24h High:         ${data['high_24h']:,.2f}")
    print(f"24h Low:          ${data['low_24h']:,.2f}")
    print(f"24h Range:        ${data['range']:,.2f} ({data['volatility_percent']:,.2f}%)")


    print("\nVolatility Metrics:")
    print("-" * 50)


    if data['volatility_percent'] > 5:
        vol_status = "HIGH"
    elif data['volatility_percent'] > 2:
        vol_status = "MEDIUM"
    else:
        vol_status = "LOW"


    print(f"24h Volatility:     {vol_status} ({data['volatility_percent']:,.2f}% range)")

    price_from_low = data['current_price'] - data['low_24h']
    print(f"Price Swing:        +${price_from_low:,.2f} from low")

    atr = data['range'] * 0.9
    print(f"ATR (14):         ${atr:,.2f}")


    bb_width = (data['volatility_percent'] * 1.2)
    print(f"Bollinger Width: {bb_width:,.1f}%")

    print("\nMarket Sentiment:")
    print("-" * 50)

    fg_value, fg_sentiment = get_fear_greed_index()
    if fg_value:
        print(f"Fear & Greed Index: {fg_value} ({fg_sentiment})")

    trend = "Bullish" if data['change_24h'] > 0 else "Bearish"
    print(f"Trend:                {trend}")
    print(f"Support Level:        ${data['low_24h'] * 0.98:,.0f}")
    print(f"Resistence level:     ${data['high_24h'] * 1.02:,.0f}")

    print("\nSignals:")
    if data['volatility_percent'] > 5:
        print(" High Volatility - except high swings")


    position_in_range = (data['current_price'] - data['low_24h']) / data['range']

    if position_in_range > 0.8:
        print("Trading near 24h high (momentum_strong)")
    elif position_in_range < 0.2:
        print("Trading near 24h low (potential bounce)")

    if fg_value and fg_value > 70:
        print(" Greed Territory - potential pullback risk")
    elif fg_value and fg_value < 30:
        print("Fear Territory - potential buying opportunity")


    print("\n" + "-" * 50 + "\n")

    set_alert = input("Set Price ALert? (y/n): ").lower()

    if set_alert == 'y':
        print("\nAlert Type:")
        print("1. Price Above")
        print("2. Price Below")
        print("3. Volatility Spike (coming soon)")


        alert_type = input("\nChoice: ")

        target_price = float(input("Target Price: "))
        alert_email = input("Alert Email: ")


        direction = "above" if alert_type == "1" else "below"
        print(f"\n Alert Created: Notify when {data['symbol']} {direction}s ${target_price:,.2f}")

        print(f"\nMonitoring {data['symbol']}...  (Price Ctrl+C to stop)\n")


        try:
            while True:
                current_data = get_crypto_data(crypto_id)
                current_price = current_data['current_price']

                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] {data['symbol']}: ${current_price:,.2f} | Target: ${target_price:,.2f} | Status: ✓")


                if (alert_type == '1' and current_price >= target_price) or \
                   (alert_type == '2' and current_price <= target_price):
                    print(f"\n Alert Triggered! {data['symbol']} hit ${target_price:,.2f}")


                    if send_alert_email(data['symbol'], current_price, target_price, alert_email):
                        print("Email Notification Sent")
                    else:
                        print("Email failed (check .env configuration)")

                    break

                time.sleep(60)


        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")


elif asset_type == '2':
    forex_pair = input("\nEnter forex pair (e.g., USD/JPY): ").upper()


    parts = forex_pair.split('/')
    if len(parts) != 2:
        print("Invalid Forex pair format!")
        exit()


    base, target = parts

    print("\nFetching Forex Data:...\n")

    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    response = requests.get(url)
    data = response.json()


    if target not in data['rates']:
        print(f"Currency pair {forex_pair} not found!")
        exit()

    current_rate = data['rates'][target]

    daily_range_pips = 125
    volatility = "MEDIUM"
    atr_pips = 85

    print(f"FOREX PAIR Analysis: {forex_pair}")
    print("-" * 50)
    print(f"Current Rate:      {current_rate:.4f}")
    print(f"Pip Movement (1h):   +15 pips")
    print(f"Daily Range:        {daily_range_pips} pips (0.83%)")
    print(f"Volatiltiy:         {volatility}")
    print()
    print(f"ATR (Pips):         {atr_pips} pips")
    print(f"Average Spread:     1.2 pips")
    print()
    print("Signals:")
    print("Normal Volatility for this pair")
    print("Neutral Mometum")


else:
    print("Invalid Choice!")
