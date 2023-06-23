import sqlite3, const
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
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

    one_day_before_isoformat = "2023-06-20"
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
        SELECT * FROM strategy
    """)

    strategies = cursor.fetchall()

    cursor.execute("""
        SELECT id, symbol, name From stock WHERE symbol = ?
    """, (symbol, ))

    
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ?
    """, (row['id'],))

    stock_prices = cursor.fetchall()
    
    return templates.TemplateResponse("stock_info.html", {"request": request, "stock": row, "bars": stock_prices, "strategies": strategies})

@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect(const.DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
    """, (stock_id, strategy_id))
    
    connection.commit()

    return RedirectResponse(url = f'/strategy/{strategy_id}', status_code = 303)

@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = sqlite3.connect(const.DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    #select name of strategy for the given strategy_id
    cursor.execute("""
        SELECT id, name
        FROM strategy
        WHERE id = ?
    """, (strategy_id,))

    strategy = cursor.fetchone()
   
    #select all stocks that applied the strategy
    cursor.execute("""
        SELECT symbol, name
        FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """, (strategy_id,))

    stocks = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request": request, "stocks": stocks, "strategy": strategy})