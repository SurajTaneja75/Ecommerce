import psycopg2
import mysql.connector
import datetime
import pandas as pd

# change credentials fefore running
host_address = 'localhost'
db_username = 'postgres'
db_password = 'password'
db_name = 'ecommerce'

def execute_query(query_name, window_type, start_date, end_date, category):
    # Connect to the PostgreSQL database
    # conn = psycopg2.connect(
    #     host=host_address,
    #     user=db_username,
    #     password=db_password,
    #     database=db_name
    # )

    # or use Mysql
    conn = mysql.connector.connect(
        host=host_address,
        user=db_username,
        password=db_password,
        database=db_name
    )
    cursor = conn.cursor()

   # List of templatized queries (Curently i have taken 3)
    queries = {
        'demand': 'SELECT * FROM ecommerce_data WHERE "InvoiceDate" BETWEEN %s AND %s AND "Description" LIKE %s',
        'price': 'SELECT * FROM ecommerce_data WHERE "InvoiceDate" BETWEEN %s AND %s AND "Description" LIKE %s',
        'customer': 'SELECT * FROM ecommerce_data WHERE "InvoiceDate" BETWEEN %s AND %s AND "Description" LIKE %s'

    }

    if query_name not in queries:
        print(f"Error: Unknown query name '{query_name}'.")
        return
    
    split_s = start_date.split("-")
    start_date = datetime.datetime(int(split_s[0]),int(split_s[1]),int(split_s[2]))
    split_e = end_date.split("-")
    end_date = datetime.datetime(int(split_e[0]),int(split_e[1]),int(split_e[2]))
    category = category.upper()


    category_with_wildcard = f'%{category}%'
    query = queries[query_name]
    cursor.execute(query, (start_date, end_date, category_with_wildcard))
    result = cursor.fetchall()

    cursor.execute('SELECT column_name FROM information_schema.columns WHERE table_name = %s',('ecommerce_data',))
    headers = cursor.fetchall()
    headers = [h[0] for h in headers]
    headers = ['id', 'InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']

    conn.close()
    df = pd.DataFrame(data=result,columns=headers)
    return df