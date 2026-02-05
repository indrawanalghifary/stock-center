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
    *   `views.py`: Application logic (Inventory, Transaction, Finance, Return).
    *   `forms.py`: Data entry forms.
    *   `signals.py`: Business logic automation (Stock deduction, Invoice creation).
    *   `admin.py`: Admin interface configuration.
    *   `urls.py`: App-specific URL routing.
*   `templates/`: Global templates directory.
    *   `base.html`: Base template with TomSelect and Lucide Icons.
    *   `home.html`: Role-based Dashboard.
    *   `inventory/`: Inventory management templates.
    *   `transaction/`: Transaction (POS) templates.
    *   `finance/`: Invoice and Payment templates.
    *   `return/`: Return Management templates.
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
*   **Searchable Items:** Integrated TomSelect for easy product lookup.
*   **Add Items:** Dynamic cart management (Draft mode).
*   **Finalize:** Lock order and trigger automation.
*   **Role-Aware:** Resellers can only create orders for themselves; Admins can create for anyone.

### 4. Finance & Receivables 💰
*   **Invoice List:** Track unpaid and partial invoices.
*   **Payments:** Record payments against invoices to reduce reseller debt.

### 5. Return Management 🔁
*   **Create Return:** Initiate return requests referencing specific invoices.
*   **Finalize Return:** Automatically restores stock and adjusts reseller balance/credit.

### 6. Role-Based Access & Dashboard 📊
*   **Admin View:** Global stock, total receivables, all transactions.
*   **Reseller View:** Personal debt, personal orders, unpaid invoices.
*   **Menu Control:** Resellers cannot see Inventory adjustment menus.

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
*   **Phase:** Feature Complete (RC1).
*   **Completed:**
    *   Core Modules: Inventory, Transaction, Finance.
    *   Advanced Features: Returns, Role Differentiation.
    *   UX: Searchable Selects, Mobile-First Design.
*   **Next Steps:**
    *   User Acceptance Testing (UAT).
    *   Deploy to production.