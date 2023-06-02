import sqlite3, const
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(const.DATABASE_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("SELECT symbol, name FROM stock")
rows = cursor.fetchall()

#create a list of symbols
symbols = [row['symbol'] for row in rows]

api = tradeapi.REST(const.API_KEY, const.SECRET_KEY, base_url=const.BASE_URL)
assets = api.list_assets()

for asset in assets:

    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            #split the assets into 2  SHIB/USD --> SHIB and USD
            split_symbols = asset.symbol.split("/")

            if len(split_symbols) == 2:
                symbol1 = split_symbols[0]
                symbol2 = split_symbols[1]
                cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (symbol1, asset.name))
                cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (symbol2, asset.name))
            else:
                cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (asset.symbol, asset.name))

    except Exception as e:
        print(asset.symbol)
        print (e)

print("finished populating the database")
connection.commit()