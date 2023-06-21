import sqlite3, const
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import date, timedelta

app = FastAPI()
templates = Jinja2Templates(directory = "templates")

#all GET requests to the '/' route
@app.get("/")
def index(request: Request):

    stock_filter = request.query_params.get('filter', False)
    #load the database when the webpage is accessed
    connection = sqlite3.connect(const.DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    one_day_before = date.today() - timedelta(days=1)  # Subtract one day from the current date
    one_day_before_isoformat = one_day_before.isoformat()  # Convert the date to ISO format

    if stock_filter == 'new_closing_highs':
        cursor.execute("""
            SELECT * from (
                select symbol, name, stock_id, max(close), date
                from stock_price join stock on stock.id = stock_price.stock_id
                group by stock_id
                order by symbol
            ) where date = ?
        """, (one_day_before_isoformat,))

    else:
        cursor.execute("""
            SELECT id, symbol, name From stock ORDER BY symbol
        """)

    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})
    # return {"Title":"dashboard","stocks": rows}

""" route for accessing a selected stock"""
@app.get("/stock/{symbol}")
def stock_info(request: Request, symbol):
    #load the database when the webpage is accessed
    connection = sqlite3.connect(const.DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, name From stock WHERE symbol = ?
    """, (symbol, ))

    
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ?
    """, (row['id'],))

    stock_prices = cursor.fetchall()
    
    return templates.TemplateResponse("stock_info.html", {"request": request, "stock": row, "bars": stock_prices})