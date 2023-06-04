# Stock-Market-Tracker
# Installation
```
pip install sqlite3
pip install alpaca-trade-api
pip3 install fastapi uvicorn
pip3 install jinja2
```
## Get API keys
To run populate_stocks.py and populate_prices.py successfully, you would need an API key and secret key inside const.py file.
The step-by-step guide is as follows:
1. Create an account on https://app.alpaca.markets/signup if you don't have an account already.
2. After logging in to the account, click on 'Generate Key' to get an API key and the secret key.
3. Make a const.py file
4. Store the following inside the file
```
import os
API_KEY = 'Your API key'
SECRET_KEY = 'Your Secret key'
DATABASE_PATH = os.path.abspath("app.db")
BASE_URL = 'https://paper-api.alpaca.markets'
```
## How to run
1. Create the stock and prices table by running the following command
```
python3 create_db.py
```
2. Store the stock data inside the database
```
python3 populate_stocks.py
```
3. Store the prices of the stocks in database
```
python3 populate_prices.py
```
4. After storing the stocks and their prices, run
```
uvicorn main:app --reload
```
5. You can start viewing the stocks on your localhost:8000 now
