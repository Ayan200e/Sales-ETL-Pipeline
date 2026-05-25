DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sales_date TEXT,
    months TEXT,
    customer_name TEXT,
    
    style_type TEXT,
    sku_code TEXT,
    product_size TEXT,
    
    pcs_quantity REAL DEFAULT 0.0,
    unit_rate REAL DEFAULT 0.0,
    gross_amt REAL DEFAULT 0.0
);

CREATE index idx_sales_date ON sales(sales_date);
CREATE index idx_customer_name ON sales(customer_name);


SELECT * FROM sales;
