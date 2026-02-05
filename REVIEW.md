# Review & Gap Analysis

Based on the requirements in `frontend.md` and `backend.md` versus the current implementation, here is a detailed breakdown of what is missing or needs improvement.

## 🚨 Critical Functional Gaps (Must Fix)

### 1. User Role Differentiation (Admin vs Affiliator/Reseller)
**Requirement:** "ada fitur login untuk owner admin, dan affiliator(yang mengambil barang)."
**Current State:**
*   The system currently treats all logged-in users effectively as Staff/Admins.
*   Any logged-in user can access the "Stock In" menu (altering warehouse inventory).
*   Any logged-in user can view the Global Dashboard (Total Receivables of *all* resellers).
*   There is no link between a Django `User` and a `Reseller` profile.

**Required Changes:**
1.  **Model Link:** Add `user = models.OneToOneField(User, ...)` to the `Reseller` model.
2.  **Access Control:**
    *   **Dashboard:** Check if `request.user` has a related `reseller` profile.
        *   *If Reseller:* Show only *their* balance, *their* active orders, and *their* unpaid invoices. Hide "Total Stock" logic or limit it to relevant items.
        *   *If Admin:* Show the current global stats.
    *   **Menu Visibility:** Hide "Stok Masuk" (Stock In) and "Semua Transaksi" menus for Resellers.
    *   **Transaction Form:**
        *   *If Reseller:* The "Reseller" field in `TransactionCreateForm` should be automatically set to the current user and hidden/read-only.
        *   *If Admin:* Can select any reseller from the dropdown.

### 2. Transaction UX (Mobile Usability)
**Requirement:** "frontend responsive mobile first"
**Current State:**
*   **Product Selection:** Uses a standard HTML `<select>` dropdown. For a store with hundreds of variants (Size/Color), scrolling through a long list on mobile is painful and error-prone.
*   **Stock Visibility:** Users cannot see the `qty_available` of a product *while* selecting it in the transaction form. They only find out it's out of stock after submitting the form and getting an error.

**Required Changes:**
*   **Searchable Dropdown:** Implement a JavaScript-based searchable select (e.g., TomSelect or a simple AJAX modal) for Product Variants.
*   **Real-time Feedback:** Display "Stok: X" next to the variant name in the dropdown or immediately after selection.

### 3. QR Code / SKU Scanning
**Requirement:** "Variant (SKU/QR)" & "Bisa scan QR SKU"
**Current State:**
*   The field `sku` exists in the database.
*   There is **no interface** to input items via camera/barcode scanner.
*   Users must manually select items from a list.

**Required Changes:**
*   **Scanner Interface:** Add a button in `TransactionDetail` view to open the camera (using a JS library like `html5-qrcode`).
*   **Logic:** When a QR is scanned, automatically find the variant and add it to the transaction list (or increment qty if already exists).

## ⚠️ UX & Visual Improvements (Nice to Have)

### 1. Invoice & Payment Flow
*   **Current:** Payments are recorded via a separate form.
*   **Improvement:** Allow partial payment directly from the Invoice Detail view. Add a "History Pembayaran" (Payment History) table on the Invoice Detail page so the user knows when and how much they paid previously.

### 2. Returns Handling (Retur)
*   **Current:** Signals exist (`core/signals.py`) to handle stock returns logic.
*   **Missing:** No **Views** or **Forms** created for initiating a Return. Users cannot currently perform a return via the UI.
*   **Required:** Create `ReturnCreateView` and `ReturnDetailView`.

### 3. Reporting
*   **Current:** Only dashboard widgets.
*   **Missing:** Detailed reports (e.g., "Sales by Product", "Stock Movement History").

## 📝 Recommended Next Steps Plan

1.  **Phase 1: User Linking:** Update `Reseller` model and run migrations.
2.  **Phase 2: Role-Based Views:**
    *   Update `home` view to split logic (Admin vs Reseller).
    *   Update `TransactionCreateView` to auto-assign reseller.
    *   Update `base.html` navigation menu.
3.  **Phase 3: Returns UI:** Build the missing views for Returns.
4.  **Phase 4: Scanning/Search:** Enhance the frontend forms with JS for better usability.
