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
    #split the assets and names into 2  SHIB/USD --> SHIB and USD
    split_symbols = asset.symbol.split("/")
    split_names = asset.name.split("/")

    for i in range(len(split_symbols)):
        try:
            if asset.status == 'active' and asset.tradable and split_symbols[i] not in symbols:
                cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)", (split_symbols[i], split_names[i], asset.exchange))

        except Exception as e:
            print(asset.symbol)
            print (e)

print("finished populating the database")
connection.commit()