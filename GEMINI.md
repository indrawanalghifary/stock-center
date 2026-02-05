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
    *   `models.py`: Database models.
    *   `views.py`: Application logic (Inventory, Transaction, Finance).
    *   `forms.py`: Data entry forms.
    *   `signals.py`: Business logic automation (Stock deduction, Invoice creation).
    *   `admin.py`: Admin interface configuration.
    *   `urls.py`: App-specific URL routing.
*   `templates/`: Global templates directory.
    *   `base.html`: Base template.
    *   `home.html`: Dashboard with statistics.
    *   `inventory/`: Inventory management templates.
    *   `transaction/`: Transaction (POS) templates.
    *   `finance/`: Invoice and Payment templates.
*   `venv/`: Python virtual environment.
*   `backend.md`: Detailed specification of the database schema and business logic.
*   `frontend.md`: User Interface and User Experience requirements.

## Key Features Implemented

### 1. Automation (The Brain) 🧠
*   **Auto-Stock Deduction:** Finalizing a transaction automatically checks and reduces warehouse stock.
*   **Auto-Invoice:** Transactions generate invoices automatically upon finalization.
*   **Auto-Ledger:** All stock changes are recorded in `StockMovement`.
*   **Reseller Balance:** Debt is automatically calculated when transactions are finalized or payments are made.

### 2. Inventory Management 📦
*   **Stock Overview:** View stock levels across all warehouses.
*   **Inbound Stock:** Form to add new stock (Purchase/Adjustment) with ledger tracking.

### 3. Transaction System (POS) 🛒
*   **Create Order:** Select Reseller and Warehouse.
*   **Add Items:** Dynamic cart management (Draft mode).
*   **Finalize:** Lock order and trigger automation.

### 4. Finance & Receivables 💰
*   **Invoice List:** Track unpaid and partial invoices.
*   **Payments:** Record payments against invoices to reduce reseller debt.

### 5. Dashboard 📊
*   **KPIs:** Total Stock, Total Receivables, Daily Transactions.
*   **Quick Actions:** Shortcuts to common tasks.

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
*   **Phase:** Functional Beta.
*   **Completed:** All core modules (Inventory, Transaction, Finance, Automation).
*   **Next Steps:**
    *   User Acceptance Testing (UAT).
    *   Refine UI/UX (Feedback loops).
    *   Add Report generation (PDF/Excel).
