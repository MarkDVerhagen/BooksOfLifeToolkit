import yaml
import pandas as pd
import os
import sqlite3
import re
import json

class Generator:
    def __init__(self, yaml_file, data_dir='data', db_name='your_database.db'):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.datasets = self.config.get('datasets', [])
        self.main_key = self.config.get('main_key', [])
        self.data_dir = data_dir
        self.db_name = db_name

        # Connect to the database
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Enable WAL mode
        self.conn.execute('PRAGMA journal_mode=WAL')

        for d in self.datasets:
            print('Now processing {}'.format(d['name']))
            data = pd.read_csv(os.path.join(self.data_dir, 'raw', d['name'] + '.csv'))
            
            structure_features = d.get('structure_features')
            structure_class = d.get('structure_classification')
            if structure_features:
                print('Adding structure features to {}'.format(d['name']))
                print(structure_features)
                data = self.pull_hierarchy(
                    data, hierarchy_vars=structure_features,
                    main_key=self.main_key, hierarchy_cat=structure_class)
            
            # Write to CSV
            data.to_csv(os.path.join(self.data_dir, 'edit', d['name'] + '.csv'), index=False)

            # Write to database
            self.write_to_db(data, d['name'])

        # Print database overview
        self.print_database_overview()

        # Commit changes and close the connection
        self.conn.commit()
        self.conn.close()
    
    def pull_hierarchy(self, data, hierarchy_vars=['HOUSEKEEPING_NR', 'DATE_STIRTHH'],
                       main_key='rinpersoon', hierarchy_cat=None):
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
        # Sanitize column names
        data.columns = [self.sanitize_column_name(col) for col in data.columns]

        # Convert all data to strings
        data = data.map(self.convert_to_string)

        # Create table
        columns = ', '.join([f'"{col}" TEXT' for col in data.columns])
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}"
                                ({columns})''')

        # Insert data
        data.to_sql(table_name, self.conn, if_exists='replace', index=False)

    @staticmethod
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
    
    @staticmethod
    def convert_to_string(val):
        if isinstance(val, (list, dict)):
            return json.dumps(val)
        return str(val)
    
    def print_database_overview(self):
        print("\nDatabase Overview:")
        print("==================")
        
        # Get list of tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get column info
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            
            print("Columns:")
            for column in columns:
                print(f"  - {column[1]} ({column[2]})")
            
            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = self.cursor.fetchone()[0]
            print(f"Row count: {row_count}")

if __name__ == "__main__":    
    # Example usage
    yaml_file = os.path.join('recipes', 'make_db.yaml')
    data_path = os.path.join('synth', 'data')
    db_name = 'synthetic_data.db'
    a = Generator(yaml_file, data_dir=data_path, db_name=db_name)