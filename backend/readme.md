# Backend Setup

## Backend structure
Backend has 2 apps:
- _**accounts**_: This is backend for user registration, authentication, etc.
- _**portfolio**_: Also backend for portfolio tracking and transactions.


## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/irakliskhirtladze/Investment-portfolio-tracker.git
   ```

2. Go to backend directory, create virtual env and activate it:
    ```sh
    cd backend
    python -m venv .venv
    source env/bin/activate  # On Linux
    .venv\Scripts\activate   # On Windows
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a .env file in the backend directory (where manage.py is located) and add the FINNHUB_API_KEY along with any other necessary environment variables:
    ```sh
    FINNHUB_API_KEY=replace_this_with_your_actual_finnhub_api_key
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```



# API usage
- A user must authenticate to use the api.

- After login, it is possible to start using the API by making cash deposit transaction first and then follow with other types 
of transactions.

- Or alternatively you can perform initial setup, which will directly insert portfolio data.
This can be done on [/api/initial-setup/]() endpoint. You can use the below example data for initial setup:

`
{    
    "cash_balance": {
        "balance": 10000
    },

    "portfolio_entries": [
        {
            "asset_type": "stock",
            "asset_symbol": "MSN",
            "quantity": 110.05555,
            "average_trade_price": 0.54
        },
        {
            "asset_type": "crypto",
            "asset_symbol": "bItcoin",
            "quantity": 10,
            "average_trade_price": 150.00
        },
        {
            "asset_type": "crypto",
            "asset_symbol": "ziLLiqa",
            "quantity": 5000,
            "average_trade_price": 0.0228
        }
    ]
}
`

Feel free to play with the data if you wish.

After this you can make other transactions as needed.

# Documentation
I have added Swagger for documenting the API endpoints. Please refer to it for more details.