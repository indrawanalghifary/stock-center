Berikut struktur final Django models untuk sistem Anda:
Multi gudang + SKU QR + stok ledger + reseller hutang + harga khusus + retur

Ini sudah setara sistem distribusi profesional.


---

🧩 1️⃣ MASTER DATA

Product

Field	Type

name	CharField
category	CharField
brand	CharField
is_active	Boolean



---

Variant

Field	Type

product	FK → Product
sku	CharField (unique)
color	CharField
size	CharField
default_price	Decimal


> QR berisi: sku




---

Warehouse

Field	Type

name	CharField
location	CharField
is_active	Boolean



---

Reseller

Field	Type

name	CharField
phone	CharField
address	TextField
credit_limit	Decimal
current_balance	Decimal



---

ResellerPrice (harga beda tiap reseller)

Field	Type

reseller	FK
variant	FK
custom_price	Decimal



---

📦 2️⃣ STOK SYSTEM

WarehouseStock (snapshot stok)

Field	Type

warehouse	FK
variant	FK
qty_available	Integer


Unique constraint: (warehouse, variant)


---

StockMovement (LEDGER) 🔥 PALING PENTING

Field	Type

warehouse	FK
variant	FK
movement_type	Choice(IN, OUT, RETURN, ADJUST)
qty	Integer (+/-)
ref_type	CharField (TRX, RETURN, OPNAME)
ref_id	Integer
user	FK User
created_at	DateTime



---

🧾 3️⃣ TRANSAKSI PENGAMBILAN RESELLER

Transaction

Field	Type

reseller	FK
warehouse	FK
user	FK User
status	Choice(DRAFT, FINAL)
created_at	DateTime



---

TransactionDetail

Field	Type

transaction	FK
variant	FK
qty	Integer
price	Decimal
subtotal	Decimal



---

💰 4️⃣ PIUTANG (ACCOUNT RECEIVABLE)

Invoice

Field	Type

reseller	FK
transaction	FK
total_amount	Decimal
paid_amount	Decimal
status	Choice(UNPAID, PARTIAL, PAID)
created_at	DateTime



---

Payment

Field	Type

reseller	FK
invoice	FK
amount	Decimal
method	CharField
created_at	DateTime



---

🔁 5️⃣ RETUR BARANG

ReturnHeader

Field	Type

reseller	FK
warehouse	FK
invoice	FK
status	Choice(DRAFT, FINAL)
created_at	DateTime



---

ReturnDetail

Field	Type

return_header	FK
variant	FK
qty	Integer



---

🔐 6️⃣ RELASI LOGIKA BISNIS

Event	Efek Sistem

Transaksi FINAL	StockMovement OUT, kurangi WarehouseStock, buat Invoice
Payment	Kurangi invoice balance, kurangi reseller.current_balance
Retur FINAL	StockMovement RETURN, tambah WarehouseStock, kurangi invoice



---

🧠 ALUR BESAR SISTEM


---

🏁 RINGKAS SUPER SINGKAT

Anda punya 5 modul utama:

1. Master Barang → Product, Variant


2. Gudang & Stok → Warehouse, WarehouseStock, StockMovement


3. Pengambilan Reseller → Transaction, TransactionDetail


4. Piutang → Invoice, Payment


5. Retur → ReturnHeader, ReturnDetail




---

Jika struktur ini dipakai, sistem Anda:

✔ Stok akurat
✔ Bisa multi gudang
✔ Bisa hutang reseller
✔ Bisa retur
✔ Bisa scan QR SKU
✔ Full audit trail


---

Langkah berikutnya paling teknis:
Saya tuliskan kode models.py Django siap pakai.
