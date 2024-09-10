# Todo API 📝

Welcome to the Todo API! This project is a FastAPI-based application for managing todo items and user authentication.

## Features ✨

- User authentication (signup, login, and token-based authentication) 🔐
- CRUD operations for todo items 🗂️
- User management (create, update, delete) 👤
- CORS configuration 🌐
- Logging with HTML formatter 📄

## Getting Started 🚀

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/bantoinese83/todo-api-fastapi.git
    cd todo-api
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    psql -U postgres -c "CREATE DATABASE todo_test_db;"
    ```

5. Configure environment variables in `.env` file:

    ```env
    APP_NAME=Todo API
    VERSION=1.0.0
    DEBUG=True
    DATABASE_URL=postgresql://user:password@localhost:5432/todo_test_db
    SECRET_KEY=your_secret_key
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ALGORITHM=HS256
    ```

### Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to `http://localhost:8000/docs` to access the interactive API documentation.

## Running Tests 🧪

1. Install test dependencies:

    ```bash
    pip install -r requirements-test.txt
    ```

2. Run the tests:

    ```bash
    pytest
    ```

## Project Structure 📂

```plaintext
.
├── app
│   ├── api
│   │   ├── auth
│   │   │   └── auth_api.py
│   │   ├── todo
│   │   │   └── todo_api.py
│   │   └── user
│   │       └── user_api.py
│   ├── core
│   │   ├── app_config.py
│   │   ├── cors_config.py
│   │   ├── events.py
│   │   ├── exceptions.py
│   │   ├── log_config.py
│   │   ├── middlewares.py
│   │   └── security.py
│   ├── db
│   │   ├── database.py
│   │   └── models.py
│   ├── schemas
│   │   ├── auth_schema.py
│   │   ├── todo_schema.py
│   │   └── user_schema.py
│   └── main.py
├── tests
│   ├── api
│   │   ├── test_auth_api.py
│   │   ├── test_todo_api.py
│   │   └── test_user_api.py
│   ├── services
│   │   ├── test_auth_services.py
│   │   ├── test_todo_service.py
│   │   └── test_user_service.py
│   ├── db
│   │   └── test_models.py
│   └── conftest.py
├── .env
├── requirements.txt
├── requirements-test.txt
└── README.md



```


