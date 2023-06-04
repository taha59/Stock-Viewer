import sqlite3, const
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory = "templates")

#all GET requests to the '/' route
@app.get("/")
def index(request: Request):
    #load the database when the webpage is accessed
    connection = sqlite3.connect(const.DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, name From stock ORDER BY symbol
    """)

    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})
    # return {"Title":"dashboard","stocks": rows}

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