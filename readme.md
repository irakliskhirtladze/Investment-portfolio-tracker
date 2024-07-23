- The API part (backend) is 99% ready functionality-wise, with some changes added periodically.
- Please consider becoming a contributor for frontend development with react framework (or other frameworks)
- Please don't hesitate to let me know any issues.

# Overview of the project
Investment portfolio tracker is meant to provide users with ability to track their existing investments with minimal effort.

## Imagine a scenario:
- You have stock investments with 2 different brokers, and you have some crypto investments on 3+ trading platforms for some reason.
- It would be pretty hard to go to 5+ different platforms to check how your investments are doing. it's even harder to get consolidated analysis of your total investments.
You would probably need to create a spreadsheet, add investments there and change current portfolio values manually every time.
## Solution
- This project should remove the need of manually setting current prices for every investment. Prices will be fetched automatically from 3rd party APIs.
- All will be done by setting initial investment amounts via making virtual transaction.
Every subsequent transaction will be needed only for reflecting actual deposit/withdrawal in investment platforms.

## Structure
This Django backend has 2 apps:
- _**accounts**_: This is backend for user registration, authentication, etc.
- _**portfolio**_: Also backend for portfolio tracking and transactions.


# Setup

### With Docker (Recommended)

1. **Clone the repository**:
    ```sh
    git clone https://github.com/irakliskhirtladze/Investment-portfolio-tracker.git
    cd Investment-portfolio-tracker
    ```

2. **Create a `.env` file** in the project root and add your environment variables (replace variables with actual values):
    ```env
    FINNHUB_API_KEY=replace_with_your_finnhub_api_key
    SECRET_KEY=replace_with_your_secret_key
    DB_NAME=portfolio_tracker
    DB_USER=replace_with_your_db_user
    DB_PASSWORD=replace_with_your_db_password
    DB_HOST=db
    DB_PORT=5432
    SITE_DOMAIN=localhost:8000
    SITE_NAME=Investment Portfolio Tracker
    ```

3. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

4. **Run migrations**:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

### Without Docker 

1. Clone the repository:
   ```sh
   git clone https://github.com/irakliskhirtladze/Investment-portfolio-tracker.git
   cd Investment-portfolio-tracker
   ```

2. Create virtual environment and activate it:
    ```sh
    python -m venv .venv
    source env/bin/activate  # On Linux
    .venv\Scripts\activate   # On Windows
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up PostgreSQL:
    - Install PostgreSQL if you haven't already.
    - Create a database and a user:
      ```sql
      CREATE DATABASE portfolio_tracker;
      CREATE USER your_db_user WITH PASSWORD 'your_db_password';
      ALTER ROLE your_db_user SET client_encoding TO 'utf8';
      ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
      ALTER ROLE your_db_user SET timezone TO 'UTC';
      GRANT ALL PRIVILEGES ON DATABASE portfolio_tracker TO your_db_user;
      ```

5. Create a .env file in the backend directory (where manage.py is located) and add the FINNHUB_API_KEY along with any other necessary environment variables:
    ```sh
    FINNHUB_API_KEY=replace_this_with_your_actual_finnhub_api_key
    SECRET_KEY=your_secret_key
    DB_NAME=portfolio_tracker
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    SITE_DOMAIN=localhost:8000
    SITE_NAME=Investment Portfolio Tracker
    ```

6. Apply migrations:
    ```sh
    python manage.py migrate
    ```

7. Set the site domain:

   ```sh
   python manage.py set_site_domain
   ```

8. Run the development server:
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