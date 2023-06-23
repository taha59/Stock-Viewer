import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import sqlite3, const
from datetime import date, datetime, timedelta

connection = sqlite3.connect(const.DATABASE_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name From stock
""")

#fetch the rows containing id symbol and the name from the stock table
rows = cursor.fetchall()

symbols = []

#make a dictionary to map the ids to the symbols so that we can do a quick lookup of ids while inserting in database
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(const.API_KEY, const.SECRET_KEY, const.BASE_URL)

chunk_size = 200
counts = {}

#loop in chunks of 200 to overcome the issue of 200 api requests per minute
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]

    # fifteenMinuteBefore = datetime.now() - timedelta(minutes=16)  # Subtract one day from the current date
    # # fifteenMinuteBefore_isoformat = fifteenMinuteBefore.isoformat()  # Convert the date to ISO format

    # print(fifteenMinuteBefore.isoformat())  # Output: YYYY-MM-DD

    barsets = api.get_bars(symbol_chunk, TimeFrame.Day, "2023-05-20", "2023-06-20")

    #store stock prices for each stock symbol
    for bar in barsets:
        try:
            print ("On symbol:", bar.S)

            stock_id = stock_dict[bar.S]

            cursor.execute("""
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (int(stock_id), bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
        except Exception as e:
            print(bar.S)

connection.commit()