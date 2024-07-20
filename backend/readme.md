- **The API part is 99% ready functionality-wise, with some changes added periodically.**
- **Please consider becoming a contributor for frontend development with react framework (or other frameworks)**
- **Please don't hesitate to let me know any issues.**

# Overview of the project
Investment portfolio tracker is meant to provide users with ability to track their existing investments with
minimal effort.

### Imagine a scenario: 
- You have stock investments with 2 different brokers, 
and you have some crypto investments on 3+ trading platforms for some reason.
- It would be pretty hard to go to 5+ different platforms to check how your investments are doing.
it's even harder to get consolidated analysis of your total investments.
- You would probably need to create a spreadsheet, add investments there and change current portfolio values manually every time.

### Solution
- This project should remove the need of manually setting current prices for every investment.
Prices will be fetched automatically from 3rd party APIs.
- All will be done by setting initial investment amounts via making virtual transaction.
- Every subsequent transaction will be needed only for reflecting actual deposit/withdrawal in investment platforms.

# Project structure
Currently, the project has 3 apps:

- _**accounts**_: This is backend for user registration, authentication, etc.
- _**portfolio**_: Also backend for portfolio tracking and transactions.
- _**web**_: Frontend achieved by django template rendering; sends requests to backend and renders templates from obtained
responses.

Backend is being built with Django and Django REST Framework.

# Setup
- Clone the repo in your local machine. Create virtual environment, activate it and run in terminal:
```
pip install -r requirements.txt
```
- Migrate 
```
python manage.py migrate
```

- Run server with:
```
python manage.py runserver
```

# API usage
- A user must authenticate to use the api.

- After login, it is possible to start using the API by making cash deposit transaction first and then follow with other types 
of transactions.

- Or alternatively you can perform initial setup, which will directly insert portfolio data.
This can be done on [/api/initial-setup/]() endpoint. You can use the below example data for initial setup:

`{
    "portfolio_entries": [
        {
            "investment_type": "stock",
            "investment_symbol": "MSN",
            "quantity": 11.05555,
            "average_trade_price": 0.54
        },
        {
            "investment_type": "crypto",
            "investment_symbol": "bItcoin",
            "quantity": 10,
            "average_trade_price": 150.00
        },
        {
            "investment_type": "crypto",
            "investment_symbol": "ziLLiqa",
            "quantity": 5000,
            "average_trade_price": 0.0228
        }
    ],
    "cash_balance": {
        "balance": 0
    }
}`

Feel free to play with the data if you wish.

After this you can make other transactions as needed.

# Documentation
I have added Swagger for documenting the API endpoints. Please refer to it for more details.
