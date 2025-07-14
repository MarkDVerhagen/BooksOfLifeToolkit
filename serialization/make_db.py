import yaml
import pandas as pd
import os
import re
import json
import argparse
import duckdb
import time

def log_general(log_file, message="Message"):
    """Logs general statement to a log file"""
    print(message)
    current_time = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))

    with open(log_file, "a") as f:
        f.write(f"{timestamp}: {message}\n")

class Generator:
    """
    Generator is responsible for generating a database as specified in a YAML configuration file, exporting them to CSV, and populating a DuckDB database.

    The class reads a configuration YAML file that specifies datasets, their features, and hierarchical structure. It processes each dataset, optionally applies hierarchical grouping, selects specified features, writes the processed data to CSV, and inserts it into a DuckDB database. It also provides utilities for column name sanitization, data conversion, and database overview printing.

    Args:
        yaml_file (str): Path (without extension) to the YAML configuration file.
        data_dir (str): Directory containing the data CSV files. Defaults to 'data'.
        db_name (str): Name of the DuckDB database file to create. Defaults to 'your_database.db'.
        table_version (str): Optional suffix for table versioning in file names.
    """
    def __init__(self, yaml_file, data_dir='data', db_name='your_database.db', table_version=""):
        """
        Initializes the Generator, processes datasets as per the YAML config, writes processed data to CSV, and populates the DuckDB database.

        Args:
            yaml_file (str): Path (without extension) to the YAML configuration file.
            data_dir (str): Directory containing the data CSV files.
            db_name (str): Name of the DuckDB database file to create.
            table_version (str): Optional suffix for table versioning in file names.
        """
        
        with open(yaml_file + '.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Get the datasets, main key, and data directory from the YAML file
        self.datasets = self.config.get('datasets', [])
        self.main_key = self.config.get('main_key', [])
        self.data_dir = data_dir
        
        # Construct the path to the database
        self.db_name = os.path.join('dbs', db_name + '.duckdb')

        # Connect to an in-memory DuckDB database
        self.conn = duckdb.connect(self.db_name)

        # Loop through the datasets, read the data, add hierarchy, extract features and write to CSV in the edit folder.
        for d in self.datasets:
            print('Now processing {}'.format(d['name']))
            data = pd.read_csv(os.path.join(self.data_dir, d['name'] + table_version + '.csv'), encoding_errors='replace')
            
            structure_features = d.get('structure_features')
            structure_class = d.get('structure_classification')
            if structure_features:
                print('Adding structure features to {}'.format(d['name']))
                print(structure_features)
                data = self.pull_hierarchy(
                    data, hierarchy_vars=structure_features,
                    main_key=self.main_key, hierarchy_cat=structure_class)
            
            features = d.get('features')
            
            if features is None:
                features = list(data.columns)
            else:
                features = features
            print(f"Collecting features: {features}")

            data = data[features]
            data['rinpersoon'] = data['rinpersoon'].astype(str)
            # Write to CSV
            data.to_csv(os.path.join(self.data_dir, 'edit', d['name'] + '.csv'), index=False)

            # Write to database
            self.write_to_db(data, d['name'])

        # Print database overview
        self.print_database_overview()

        # Close the in-memory connection
        self.conn.close()

        # Verify the exported database
        try:
            verify_conn = duckdb.connect(self.db_name)
            tables = verify_conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
            print(f"Verified tables in exported database: {[table[0] for table in tables]}")
            verify_conn.close()
        except Exception as e:
            print(f"Error verifying exported database: {e}")
    
    def pull_hierarchy(self, data, hierarchy_vars=['HUISHOUDNR', 'DATUMAANVANGHH'],
                       main_key='rinpersoon', hierarchy_cat=None):
        """
        Adds hierarchical grouping to the dataset based on specified variables. It is assumed there is a main key in the dataset.
        Per row, all main keys are fetched based on the hierarchy variables.

        Args:
            data (pd.DataFrame): The input DataFrame.
            hierarchy_vars (list): List of columns based on which to define the hierarchy.
            main_key (str): The main key to fetch based on the hierarchy.
            hierarchy_cat (str, optional): Additional category for hierarchy grouping and pivoting.

        Returns:
            pd.DataFrame: DataFrame with added hierarchical columns.
        """
        ## Function to pull in main keys based on a hierarchy variable
        
        # Make hierarchy variable
        data['hierarchy'] = data.\
            apply(lambda row: '_'.join([str(row[var]) for var in hierarchy_vars]), axis=1)
            
        # Group by hierarchy and additional var
        hierarchy_list = ['hierarchy']
        if hierarchy_cat:
            hierarchy_list.append(hierarchy_cat)

        grouped = data.groupby(hierarchy_list).agg({main_key: list}).reset_index()

        # Pivot table
        if hierarchy_cat:
            grouped = grouped.pivot(index='hierarchy', columns=hierarchy_cat, values=main_key).reset_index()

        # Rename columns
        grouped.columns.name = None
        grouped.columns = ['hierarchy'] + [f'ID_list_{col}' for col in grouped.columns if col != 'hierarchy']
        return pd.merge(data, grouped)

    def write_to_db(self, data, table_name):
        """
        Writes a DataFrame to the DuckDB database as a table.

        Args:
            data (pd.DataFrame): The DataFrame to write.
            table_name (str): The name of the table in the database.
        """
        # Sanitize column names
        data.columns = [self.sanitize_column_name(col) for col in data.columns]

        # Convert all data to strings
        data = data.map(self.convert_to_string)

        # Create table and insert data
        self.conn.register('temp_df', data)
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM temp_df")
        self.conn.unregister('temp_df')

    @staticmethod
    def sanitize_column_name(name):
        """
        Sanitizes a column name to be compatible with SQL table requirements.

        Args:
            name (str): The original column name.

        Returns:
            str: The sanitized column name.
        """
        # Remove any character that's not a letter, number, or underscore
        name = re.sub(r'[^\w]', '_', name)
        # Ensure the name doesn't start with a number
        if name[0].isdigit():
            name = '_' + name
        # Avoid SQLite keywords
        sqlite_keywords = ['ADD', 'ALL', 'ALTER', 'AND', 'AS', 'AUTOINCREMENT', 'BETWEEN', 'CASE',
                           'CHECK', 'COLLATE', 'COMMIT', 'CONSTRAINT', 'CREATE', 'DEFAULT', 'DEFERRABLE',
                           'DELETE', 'DISTINCT', 'DROP', 'ELSE', 'ESCAPE', 'EXCEPT', 'EXISTS', 'FOREIGN',
                           'FROM', 'GROUP', 'HAVING', 'IN', 'INDEX', 'INSERT', 'INTERSECT', 'INTO', 'IS',
                           'ISNULL', 'JOIN', 'LIMIT', 'NOT', 'NOTNULL', 'NULL', 'ON', 'OR', 'ORDER',
                           'PRIMARY', 'REFERENCES', 'SELECT', 'SET', 'TABLE', 'THEN', 'TO', 'TRANSACTION',
                           'UNION', 'UNIQUE', 'UPDATE', 'USING', 'VALUES', 'WHEN', 'WHERE']
        if name.upper() in sqlite_keywords:
            name = '_' + name
        return name
    
    @staticmethod
    def convert_to_string(val):
        """
        Converts a value to a string, serializing lists and dicts as JSON.

        Args:
            val: The value to convert.

        Returns:
            str: The string representation of the value.
        """
        if isinstance(val, (list, dict)):
            return json.dumps(val)
        return str(val)
    
    def print_database_overview(self):
        """
        Prints an overview of the tables and columns in the DuckDB database, including row counts for each table.
        """
        print("\nDatabase Overview:")
        print("==================")
        
        # Get list of tables
        tables = self.conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get column info
            columns = self.conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            
            print("Columns:")
            for column in columns:
                print(f"  - {column[1]} ({column[2]})")
            
            # Get row count
            row_count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate a DuckDB database with data')
    parser.add_argument('--data_dir', type=str, help='Path to data directory')
    parser.add_argument('--yaml_file', type=str, help='Path to the YAML configuration file')
    parser.add_argument('--db_name', type=str, default=None, help='Name of the DuckDB database')
    parser.add_argument('--log_file', type=str, default=None, help='Log file to record database population duration')
    parser.add_argument('--table_version', type=str, default="", help='Table version to load')
    args = parser.parse_args()

    if not args.yaml_file:
        raise ValueError("The --yaml_file argument is required.")

    db_name = args.db_name if args.db_name else (args.yaml_file.split("/make_")[-1] + args.table_version + '.duckdb')
    log_file = args.log_file if args.log_file else (args.yaml_file.split("recipes/")[-1] + args.table_version + '.log')
    log_file = os.path.join('logs', log_file)

    print(f"Logging at: {log_file}")
    log_general(log_file, f"Starting to prepare data and make a database according to {args.yaml_file}.\n")
    a = Generator(args.yaml_file, data_dir=args.data_dir, db_name=db_name, table_version=args.table_version)
    log_general(log_file, f"Finished generating database {db_name}.\n")