# Stock-Market-Tracker
# Installation
```
pip install sqlite3
pip install alpaca-trade-api
```
## Get API keys
To run populate_db.py successfully, you would need an API key and secret key inside creds.py file.
The step-by-step guide is as follows:
1. Create an account on https://app.alpaca.markets/signup if you don't have an account already.
2. After logging in to the account, click on 'Generate Key' to get an API key and the secret key.
3. Make a creds.py file
4. Store the following inside the file
```
API_KEY = 'Your API key'
SECRET_KEY = 'Your Secret key'
```
5. Now you can run populate_db.py successfully!
