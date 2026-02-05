# Stock Center Development Roadmap

## 🧠 Phase 1: Business Logic & Automation (The Brain)
*These tasks ensure the system behaves correctly behind the scenes.*

- [x] **Setup Signals (`core/signals.py`)**
    - [x] Create `transaction_finalized` logic:
        - [x] Verify sufficient stock availability.
        - [x] Deduct `qty_available` from `WarehouseStock`.
        - [x] Create `StockMovement` record (Type: OUT).
        - [x] Automatically create `Invoice` from `Transaction`.
    - [x] Create `payment_received` logic:
        - [x] Update `Invoice.paid_amount` and `Invoice.status`.
        - [x] Update `Reseller.current_balance` (Reduce debt).
    - [x] Create `return_finalized` logic:
        - [x] Add `qty` back to `WarehouseStock`.
        - [x] Create `StockMovement` record (Type: RETURN).
        - [x] Adjust `Invoice` or `Reseller` balance.
- [x] **App Configuration**
    - [x] Register signals in `core/apps.py`.

## 📦 Phase 2: Inventory Management (Stock In)
*Before selling, we need to get goods into the warehouse.*

- [x] **Forms (`core/forms.py`)**
    - [x] Create `StockAdjustmentForm` (for Initial Stock / Opname / Restock).
- [x] **Views (`core/views.py`)**
    - [x] Create `InventoryListView` (Overview of stock per warehouse).
    - [x] Create `StockInView` (Process to add stock from Supplier/Production).
- [x] **Templates**
    - [x] `inventory/list.html`: Table showing Product, Variant, Warehouse, Qty.
    - [x] `inventory/stock_in.html`: Form to select Warehouse, Variant, and Qty to add.

## 🧾 Phase 3: Transaction System (POS)
*The core flow for selling to resellers.*

- [x] **Forms**
    - [x] `TransactionCreateForm`: Select Reseller & Warehouse.
    - [x] `TransactionDetailForm`: Add Product/Variant & Qty.
- [x] **Views**
    - [x] `TransactionListView`: List of all transactions with filters (Draft/Final).
    - [x] `TransactionCreateView`: Start a new order.
    - [x] `TransactionUpdateView`: Add items to the Draft order.
    - [x] `TransactionFinalizeView`: Action to lock order and trigger Phase 1 logic.
- [x] **Templates**
    - [x] `transaction/create.html`: Simple header form.
    - [x] `transaction/detail.html`: Interface to add items (search product) and show total.

## 💰 Phase 4: Finance & Receivables
*Tracking money and debts.*

- [x] **Views**
    - [x] `InvoiceListView`: List unpaid/partial invoices.
    - [x] `PaymentCreateView`: Form to record payment for a specific Invoice.
- [x] **Templates**
    - [x] `finance/invoice_list.html`: Tables with "Pay Now" buttons.
    - [x] `finance/payment_form.html`: Input amount and method.

## 📊 Phase 5: Dashboard & Reporting
- [x] **Dashboard View**
    - [x] Calculate Total Stock Value.
    - [x] Calculate Total Receivables (Piutang).
    - [x] Show Recent Transactions.
- [x] **Dashboard Template**
    - [x] Use DaisyUI Stats components for KPIs.

## 🔐 Phase 6: Access Control
- [x] Implement `LoginRequiredMixin` globally.
- [x] Differentiate views/menus for `is_staff` (Admin/Owner) vs Standard Users (Staff/Reseller optional).