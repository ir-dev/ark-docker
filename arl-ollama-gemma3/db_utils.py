import sqlite3
import os

# DB_PATH = r"./data/ark_play.db"
DB_PATH = os.environ.get('DATA_FILE_PATH', r'./data/ark_play.db')
def get_trending_products(intent_data):
    category = intent_data.get("category", "products")
    table = "gpo"
    qty_col = "fg_qty"
    date_col = "fg_datetime"
    top_n = intent_data.get("quantity", 3)
    start_date = intent_data.get("start_date", "")
    end_date = intent_data.get("end_date", "")

    # Different extraction based on category
    if category == "products":
        item_expr = "json_extract(fin_goods_, '$.fg_number')"
    elif category == "machines":
        item_expr = "machine_uid"
    else:
        # Default to products if unknown
        item_expr = "json_extract(fin_goods_, '$.fg_number')"

    query = f"""
    SELECT {item_expr} AS item_id, SUM({qty_col}) AS total_quantity
    FROM {table}
    WHERE 1=1
    """
    if start_date:
        query += f" AND date({date_col}) >= date('{start_date}')"
    if end_date:
        query += f" AND date({date_col}) <= date('{end_date}')"

    query += f" GROUP BY item_id ORDER BY total_quantity DESC LIMIT {top_n}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    trending = [{"fg_number" if category == "products" else "machine_id": row[0], "total_ordered": row[1]} for row in results]
    return trending