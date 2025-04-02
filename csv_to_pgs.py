import psycopg2
import csv
import pandas as pd

def infer_data_type(column_name, sample_value):
    if pd.api.types.is_integer_dtype(sample_value):
        return 'NUMERIC'
    elif pd.api.types.is_float_dtype(sample_value):
        return 'NUMERIC'
    elif pd.api.types.is_datetime64_any_dtype(sample_value):
        return 'DATE'
    elif 'time' in column_name.lower() and ":" in str(sample_value):  
        return 'TIME'
    else:
        return 'TEXT'

# Database connection parameters
db_params = {
    'dbname': 'testdb',
    'user': 'postgres',
    'password': 'aadit@11',
    'host': 'localhost',
    'port': '5432'
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()


csv_path = 'local.csv'
first_row = pd.read_csv(csv_path, nrows=1).iloc[0]
columns = first_row.index.tolist()

table_creation_query = "CREATE TABLE digipay_temp_table5 (" + ", ".join([f'"{col}" TEXT' for col in columns]) + ");"
cur.execute(table_creation_query)

# Load data from CSV into the table
copy_sql = '''
COPY digipay_temp_table5 FROM stdin WITH CSV HEADER
DELIMITER as ','
'''
with open(csv_path, 'r') as f:
    cur.copy_expert(sql=copy_sql, file=f)
conn.commit()

# Create a view based on the table
view_creation_query = '''
CREATE VIEW digipay_iso.History_Table AS SELECT * FROM digipay_temp_table5;
'''
cur.execute(view_creation_query)
conn.commit()

cur.close()
conn.close()