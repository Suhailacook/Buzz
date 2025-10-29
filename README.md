# 📦 Inventory Management System (Flask Web App)

This is a simple, local-first inventory management system built with Python and Flask. It uses an SQLite database to store inventory and sales data, and provides a web interface for easy management.

## ✨ Features

*   **Dashboard**: View all items, current stock, and total inventory value.
*   **Add New Item**: Add new products to your inventory with initial stock and cost.
*   **Record Sale**: Manually enter daily sales, which automatically updates the stock quantity.
*   **Sales History**: View a log of all recorded sales.
*   **Stock Management**: Edit stock quantity and delete items directly from the dashboard.
*   **Export**: Export the current inventory to a neatly formatted Excel file (`.xlsx`).
*   **Local & Offline**: Runs entirely on your local machine and does not require an internet connection after setup.

## 🛠️ Setup and Installation

### Prerequisites

You need **Python 3** installed on your system.

### Installation Steps

1.  **Navigate to the project directory:**
    \`\`\`bash
    cd /home/ubuntu/Buzz
    \`\`\`

2.  **Install the required Python packages:**
    \`\`\`bash
    pip3 install -r requirements.txt
    \`\`\`

    *Note: The main dependencies are \`Flask\` for the web server and \`openpyxl\` for Excel export.*

## 🚀 Running the Application

1.  **Start the Flask application:**
    \`\`\`bash
    python3 app.py
    \`\`\`

2.  **Access the application:**
    Open your web browser and go to:
    [http://localhost:5000](http://localhost:5000)

The application will automatically create the database file (`store.db`) and the necessary tables upon first run.

## 📝 Usage Guide

### 1. Dashboard (`/`)

*   This is the main view. It shows a summary of your inventory (Total Items, Total Quantity, Total Value).
*   The table lists all items, their current quantity, cost, and the last time they were updated.
*   **Export Button**: Click the **"📥 Export to Excel"** button to download a spreadsheet of your current inventory.
*   **Actions**: Use the **"✏️ Edit"** button to quickly change the stock quantity, or **"🗑️ Delete"** to remove an item.

### 2. Add New Item (`/add_item`)

*   Use this page when you receive new stock or want to track a new product.
*   Enter the **Item Name** (must be unique), the **Initial Quantity**, and the **Cost per Unit**.

### 3. Record Sale (`/add_sale`)

*   Use this page to log daily sales.
*   **Select Item**: Choose the item that was sold from the dropdown. The available stock will be shown.
*   **Quantity Sold**: Enter the number of units sold.
*   Click **"Record Sale"**. The stock will be automatically deducted from the inventory.

### 4. Sales History (`/sales_history`)

*   View a chronological list of all sales transactions recorded in the system.

## 🗃️ Database Structure

The system uses a single SQLite file named \`store.db\` with two tables:

| Table Name | Description |
| :--- | :--- |
| \`inventory\` | Stores the current stock levels and item details. |
| \`sales\` | Stores a log of every recorded sale transaction. |

### \`inventory\` Table Schema

| Column | Type | Description |
| :--- | :--- | :--- |
| \`item_id\` | INTEGER (PK) | Unique identifier for the item. |
| \`item_name\` | TEXT (UNIQUE) | Name of the product. |
| \`quantity\` | INTEGER | Current stock quantity. |
| \`cost\` | REAL | Cost per unit (used for total value calculation). |
| \`last_update\` | TIMESTAMP | Date and time of the last stock update. |

### \`sales\` Table Schema

| Column | Type | Description |
| :--- | :--- | :--- |
| \`sale_id\` | INTEGER (PK) | Unique identifier for the sale record. |
| \`item_id\` | INTEGER (FK) | Foreign key linking to the \`inventory\` table. |
| \`quantity_sold\` | INTEGER | Number of units sold in this transaction. |
| \`sale_date\` | TIMESTAMP | Date and time the sale was recorded. |
