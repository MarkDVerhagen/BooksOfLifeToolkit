import pandas as pd
import yaml
import duckdb
import os
import argparse
import re
import json

def write_to_db(conn, data, table_name):
        # Sanitize column names
        data.columns = [sanitize_column_name(col) for col in data.columns]

        # Convert all data to strings
        data = data.map(convert_to_string)

        # Create table and insert data
        conn.register('temp_df', data)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM temp_df")
        conn.unregister('temp_df')

def sanitize_column_name(name):
    # Remove any character that's not a letter, number, or underscore
    name = re.sub(r'[^\w]', '_', name)
    # Ensure the name doesn't start with a number
    if name[0].isdigit():
        name = '_' + name
    # Avoid SQLite keywords
    sqlite_keywords = ['ADD', 'ALL', 'ALTER', 'AND', 'AS', 'AUTOINCREMENT', 'BETWEEN', 'CASE', 'CHECK', 'COLLATE', 'COMMIT', 'CONSTRAINT', 'CREATE', 'DEFAULT', 'DEFERRABLE', 'DELETE', 'DISTINCT', 'DROP', 'ELSE', 'ESCAPE', 'EXCEPT', 'EXISTS', 'FOREIGN', 'FROM', 'GROUP', 'HAVING', 'IN', 'INDEX', 'INSERT', 'INTERSECT', 'INTO', 'IS', 'ISNULL', 'JOIN', 'LIMIT', 'NOT', 'NOTNULL', 'NULL', 'ON', 'OR', 'ORDER', 'PRIMARY', 'REFERENCES', 'SELECT', 'SET', 'TABLE', 'THEN', 'TO', 'TRANSACTION', 'UNION', 'UNIQUE', 'UPDATE', 'USING', 'VALUES', 'WHEN', 'WHERE']
    if name.upper() in sqlite_keywords:
        name = '_' + name
    return name

def convert_to_string(val):
    if isinstance(val, (list, dict)):
        return json.dumps(val)
    return str(val)

def print_database_overview(conn):
    print("\nDatabase Overview:")
    print("==================")
    
    # Get list of tables
    tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get column info
        columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        
        print("Columns:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        # Get row count
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Row count: {row_count}")

def populate_db(yaml_file, db_name='your_database.db'):
    with open(os.path.join('recipes', f'{yaml_file}.yaml'), 'r') as file:
        config = yaml.safe_load(file)
        datasets = config.get('datasets', [])
        main_key = config.get('main_key', [])
    
    # Connect to an in-memory DuckDB database
    conn = duckdb.connect(db_name)

    for d in datasets:
        print(f"Processing {d['name']}...")
        # Load data
        data = pd.read_csv(os.path.join('synth', 'data', 'edit', d['name'] + '.csv'))

        # Write to database
        write_to_db(conn, data, d['name'])

    # Print database overview
    print_database_overview(conn)

    # Close the in-memory connection
    conn.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Populate a DuckDB database with data')
    parser.add_argument('--yaml_file', type=str, help='Path to the YAML configuration file')
    parser.add_argument('--db_name', type=str, default='synthetic_data.duckdb', help='Name of the DuckDB database')
    args = parser.parse_args()

    populate_db(args.yaml_file, args.db_name)