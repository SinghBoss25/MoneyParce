# MoneyParce

## Overview

MoneyParce is a personal finance management web application built with the Django framework. It provides a comprehensive suite of tools to help you take control of your financial life. Track your income and expenses, set budgets, and gain valuable insights into your spending habits through dynamic graphs and real-time data visualizations.

The application leverages RESTful APIs for secure financial transactions and offers the flexibility of both automatic bank data synchronization and manual entry.

---

## Features

* **Income & Expense Tracking:** Easily record all your financial activities, categorizing them for better understanding.
* **Budget Management:** Set monthly or category-specific budgets to stay on top of your spending goals.
* **Data Visualization:** Interactive charts and graphs provide a clear visual representation of your financial health.
* **Bank Synchronization:** Securely connect your bank accounts for automatic transaction updates through our robust API integration.
* **Manual Entry:** Maintain control and privacy by manually inputting your financial data.
* **Secure Transactions:** Our RESTful API design ensures that your financial data is handled with the utmost security.

---

## Technologies Used

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL (or your preferred database)
* **Frontend:** (Specify your frontend technologies, e.g., React, Vue.js, or standard Django templates)
* **API:** RESTful architecture

---

## Installation

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.x
* Pip
* Git

### Steps

1.  **Clone the repo**
    ```sh
    git clone [https://github.com/your_username/MoneyParce.git](https://github.com/your_username/MoneyParce.git)
    ```
2.  **Navigate to the project directory**
    ```sh
    cd MoneyParce
    ```
3.  **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```
5.  **Set up the database**
    ```sh
    python manage.py migrate
    ```
6.  **Run the development server**
    ```sh
    python manage.py runserver
    ```

---

## API Endpoints

MoneyParce exposes a set of RESTful endpoints for managing your financial data.

* `POST /api/transactions/`: Create a new transaction.
* `GET /api/transactions/`: Retrieve a list of all transactions.
* `GET /api/transactions/{id}/`: Get details of a specific transaction.
* `PUT /api/transactions/{id}/`: Update a transaction.
* `DELETE /api/transactions/{id}/`: Delete a transaction.
* `GET /api/budgets/`: Retrieve budget information.
* `POST /api/budgets/`: Set a new budget.
* `GET /api/graph-data/`: Fetch data for financial visualizations.
