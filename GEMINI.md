# Stock Center Project

## Overview
This project is a stock management system designed for multi-warehouse operations, reseller management (credit/debt), and comprehensive stock tracking (ledger system).

## Architecture
*   **Backend:** Django 5.2.10 (Python)
*   **Frontend:** Mobile-first responsive web interface using Django Templates, styled with Tailwind CSS and DaisyUI.
*   **Database:** SQLite (default for development), capable of scaling to PostgreSQL.

## Directory Structure
*   `config/`: Main Django project configuration (settings, URLs).
*   `core/`: Main application containing business logic and models.
    *   `models.py`: Contains all database models (Product, Variant, Warehouse, Stock, Transaction, etc.).
    *   `admin.py`: Admin interface configuration.
    *   `views.py`: Basic views (Home).
    *   `urls.py`: App-specific URL routing.
*   `templates/`: Global templates directory.
    *   `base.html`: Base template with Tailwind/DaisyUI and Lucide Icons.
    *   `home.html`: Homepage template.
    *   `login.html`: Login page template.
*   `venv/`: Python virtual environment.
*   `backend.md`: Detailed specification of the database schema and business logic.
*   `frontend.md`: User Interface and User Experience requirements.

## Key Specifications
*   **Models Implemented:**
    *   **Master Data:** Product, Variant (SKU/QR), Warehouse, Reseller, ResellerPrice.
    *   **Stock System:** WarehouseStock, StockMovement (Ledger).
    *   **Transactions:** Transaction, TransactionDetail.
    *   **Receivables:** Invoice, Payment.
    *   **Returns:** ReturnHeader, ReturnDetail.
*   **Frontend:**
    *   Responsive layout with DaisyUI.
    *   Login/Logout functionality.
    *   Lucide Icons integration.

## Setup & Running

### Prerequisites
*   Python 3.12+
*   Active Virtual Environment (`source venv/bin/activate`)

### Commands
1.  **Activate Environment:**
    ```bash
    source venv/bin/activate
    ```
2.  **Run Development Server:**
    ```bash
    python manage.py runserver
    ```
3.  **Database Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Create Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

## Development Status
*   **Phase:** Foundation Complete.
*   **Completed:**
    *   Database schema implementation (`core/models.py`).
    *   Admin interface registration (`core/admin.py`).
    *   Basic frontend structure (`templates/base.html`).
    *   Authentication views (Login/Logout).
*   **Next Steps:**
    *   Implement specific business logic (Stock ledger updates on transaction finalization).
    *   Create dashboards for different user roles (Owner vs Reseller).
    *   Build forms for data entry (Product, Warehouse, Transaction).