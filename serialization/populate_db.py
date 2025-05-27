import pandas as pd
import yaml
import duckdb
import os
import argparse
import re
import json
import time

def log_general(log_file, message="Message"):
    """Logs general statement to a log file"""
    print(message)
    current_time = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))

    with open(log_file, "a") as f:
        f.write(f"{timestamp}: {message}\n")

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
    with open(yaml_file + '.yaml', 'r') as file:
        config = yaml.safe_load(file)
        datasets = config.get('datasets', [])
        main_key = config.get('main_key', [])
    
    # Connect to an in-memory DuckDB database
    conn = duckdb.connect(os.path.join('dbs', db_name))

    for d in datasets:
        print(f"Processing {d['name']}...")
        # Load data
        data = pd.read_csv(os.path.join('data', 'edit', d['name'] + '.csv'))

        # Write to database
        write_to_db(conn, data, d['name'])

    # Print database overview
    print_database_overview(conn)

    # Close the in-memory connection
    conn.close()

 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Populate a DuckDB database with data')
    parser.add_argument('--yaml_file', type=str, help='Path to the YAML configuration file')
    parser.add_argument('--db_name', type=str, default=None, help='Name of the DuckDB database')
    parser.add_argument('--log_file', type=str, default=None, help='Log file to record database population duration')
    parser.add_argument('--table_version', type=str, default="", help='Table version to load')
    args = parser.parse_args()

    db_name = args.db_name if args.db_name else (args.yaml_file.split("/make_")[-1] + args.table_version + '.duckdb')
    log_file = args.log_file if args.log_file else (args.yaml_file.split("recipes/")[-1] + args.table_version + '.log')
    log_file = os.path.join('logs', log_file)
    
    log_general(log_file, f"Starting to populate database {db_name}.\n")
    populate_db(args.yaml_file, db_name)
    log_general(log_file, f"Finished populating database {db_name}.\n")