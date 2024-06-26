- **This is a work-in-progress project.**
- **Please don't hesitate to let me know any issues.**
- **And please consider becoming a contributor, especially for frontend development, since I build mostly backend.**

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



