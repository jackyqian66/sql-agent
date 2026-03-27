import sqlite3
import os

def create_sample_database():
    db_path = "data/sales.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            sales_amount REAL,
            month TEXT,
            quarter TEXT,
            year INTEGER
        )
    ''')
    
    sales_data = [
        (1, "Product A", 350000, "July", "Q3", 2024),
        (2, "Product B", 280000, "July", "Q3", 2024),
        (3, "Product C", 220000, "July", "Q3", 2024),
        (4, "Product A", 360000, "August", "Q3", 2024),
        (5, "Product B", 270000, "August", "Q3", 2024),
        (6, "Product C", 230000, "August", "Q3", 2024),
        (7, "Product A", 340000, "September", "Q3", 2024),
        (8, "Product B", 290000, "September", "Q3", 2024),
        (9, "Product C", 210000, "September", "Q3", 2024),
    ]
    
    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', sales_data)
    
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            customer_name TEXT,
            email TEXT,
            signup_date TEXT
        )
    ''')
    
    customers_data = [
        (1, "Customer 1", "customer1@example.com", "2024-01-15"),
        (2, "Customer 2", "customer2@example.com", "2024-02-20"),
        (3, "Customer 3", "customer3@example.com", "2024-03-10"),
        (4, "Customer 4", "customer4@example.com", "2024-04-05"),
        (5, "Customer 5", "customer5@example.com", "2024-05-12"),
    ]
    
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers_data)
    
    conn.commit()
    conn.close()
    
    print(f"数据库已创建: {db_path}")
    print(f"销售记录数: {len(sales_data)}")
    print(f"客户记录数: {len(customers_data)}")

if __name__ == "__main__":
    create_sample_database()
