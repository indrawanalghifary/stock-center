# Stock Center Project

## Overview
This project is a stock management system designed for multi-warehouse operations, reseller management, comprehensive stock tracking, and integrated packing labor tracking.

## Architecture
*   **Backend:** Django 5.2.10 (Python)
*   **Frontend:** Mobile-first responsive web interface using Django Templates, styled with Tailwind CSS and DaisyUI.
*   **Database:** SQLite (default for development), capable of scaling to PostgreSQL.

## Directory Structure
*   `config/`: Main Django project configuration.
*   `core/`: Main application containing business logic, models, and scanner processing.
*   `templates/`: Global templates (Inventory, Transaction, Finance, Return, Packing, Scanner).
*   `static/`: Static assets (Icons, CSS).

## Key Features Implemented

### 1. Automation & Scanner (The Brain) 🧠
*   **Advanced Batch Scanner:** Continuous scanning mode for high-speed SKU processing.
*   **Multi-Mode Scanner:**
    *   **Packing Mode:** Logs packing labor, SKU counts, and calculates fees/incentives.
    *   **Stock Mode:** Direct warehouse stock updates (Opname) via barcode.
    *   **Order Mode:** Instant transaction creation from scanned batch.
*   **Real-time SKU Validation:** Instant database lookup during scanning with visual feedback.
*   **Torch Control:** Integrated flashlight support for low-light scanning environments.

### 2. Packing Management 📦
*   **Labor Tracking:** Records who performed the packing, when, and where.
*   **Fee Calculation:** Automatic calculation of packing fees based on item count.
*   **Activity History:** Searchable and filterable history of all packing tasks.

### 3. Inventory & Stock 🏢
*   **Warehouse Overview:** Real-time stock levels across multiple locations.
*   **Ledger System:** Every movement (In, Out, Return, Scan) is logged in `StockMovement`.
*   **Auto-Stock Deduction:** Finalized transactions automatically reduce stock.

### 4. Transaction & Finance 💰
*   **Deep Linking:** Seamless navigation between Transactions and their associated Invoices.
*   **Payment System:** Records payments with dropdown methods (Cash, Transfer, E-Wallet) and tracks remaining balances.
*   **Reseller Balance:** Automated debt/credit calculation for resellers.

### 5. Return Management 🔁
*   **Invoice-Linked Returns:** Returns are validated against original invoice quantities.
*   **Auto-Adjustment:** Finalizing returns restores stock and adjusts reseller balances.

## Setup & Running

### Prerequisites
*   Python 3.12+
*   Active Virtual Environment (`source venv/bin/activate`)

### Commands
1.  **Run Development Server:** `python manage.py runserver`
2.  **Database Migrations:** `python manage.py migrate`
3.  **System Check:** `python manage.py check`

## Development Status
*   **Phase:** Feature Complete (RC2).
*   **Latest Additions:** Advanced Batch Scanner, Packing Labor Module, Transaction-Invoice Deep Linking.
