import sqlite3, const

connection = sqlite3.connect(const.DATABASE_PATH)
cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price
""")

cursor.execute("""
    DROP TABLE stock
""")

connection.commit()