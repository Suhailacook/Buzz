import sqlite3
import os
from datetime import datetime

DATABASE_FILE = 'store.db'

def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            cost REAL NOT NULL DEFAULT 0.0,
            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            quantity_sold INTEGER NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES inventory(item_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_item(item_name, quantity, cost):
    """Add a new item to inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO inventory (item_name, quantity, cost, last_update)
            VALUES (?, ?, ?, ?)
        ''', (item_name, quantity, cost, datetime.now()))
        conn.commit()
        return True, "Item added successfully!"
    except sqlite3.IntegrityError:
        return False, "Item already exists!"
    finally:
        conn.close()

def record_sale(item_id, quantity_sold):
    """Record a sale and update inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get current quantity
        cursor.execute('SELECT quantity FROM inventory WHERE item_id = ?', (item_id,))
        result = cursor.fetchone()
        
        if not result:
            return False, "Item not found!"
        
        current_quantity = result['quantity']
        
        if current_quantity < quantity_sold:
            return False, f"Insufficient stock! Available: {current_quantity}"
        
        # Record the sale
        cursor.execute('''
            INSERT INTO sales (item_id, quantity_sold, sale_date)
            VALUES (?, ?, ?)
        ''', (item_id, quantity_sold, datetime.now()))
        
        # Update inventory
        new_quantity = current_quantity - quantity_sold
        cursor.execute('''
            UPDATE inventory
            SET quantity = ?, last_update = ?
            WHERE item_id = ?
        ''', (new_quantity, datetime.now(), item_id))
        
        conn.commit()
        return True, f"Sale recorded! New quantity: {new_quantity}"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_all_items():
    """Get all items from inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory ORDER BY item_name')
    items = cursor.fetchall()
    conn.close()
    return items

def get_item_by_id(item_id):
    """Get a specific item by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE item_id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def get_sales_history():
    """Get all sales records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.sale_id, i.item_name, s.quantity_sold, s.sale_date
        FROM sales s
        JOIN inventory i ON s.item_id = i.item_id
        ORDER BY s.sale_date DESC
    ''')
    sales = cursor.fetchall()
    conn.close()
    return sales

def delete_item(item_id):
    """Delete an item from inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM inventory WHERE item_id = ?', (item_id,))
        conn.commit()
        return True, "Item deleted successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def update_item_quantity(item_id, new_quantity):
    """Update the quantity of an item."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE inventory
            SET quantity = ?, last_update = ?
            WHERE item_id = ?
        ''', (new_quantity, datetime.now(), item_id))
        conn.commit()
        return True, "Quantity updated successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()
