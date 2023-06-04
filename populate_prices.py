import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import sqlite3, const

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

#loop in chunks of 200 to evade overcome the issue of 200 api requests at a time
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_bars(symbol_chunk, TimeFrame.Day, "2023-05-31", "2023-05-31")

    #store stock prices for each stock symbol
    counts = {}
    for bar in barsets:

        if bar.S not in counts or counts[bar.S] == 1:
            print ("On symbol:", bar.S)

            stock_id = stock_dict[bar.S]

            cursor.execute("""
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (int(stock_id), bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
        

        if bar.S in counts:
            counts[bar.S] += 1
        else:
            counts[bar.S] = 1

connection.commit()