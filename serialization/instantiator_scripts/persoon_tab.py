import duckdb
import sqlite3
from typing import Dict, Any
from serialization.instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph

# def get_person_attributes(rinpersoon: str, db_name: str = 'synthetic_data.duckdb', table_version: str = '') -> PersonAttributesParagraph: ## 20/8
def get_person_attributes(rinpersoon: str, conn, table_version: str = '') -> PersonAttributesParagraph: ## 20/8
    """
    This function loads personal attributes for a given rinpersoon (person_id)
    by querying the SQLite database and creating the PersonAttributesParagraph object.
    """
    # conn = duckdb.connect(db_name, read_only=True) ## 20/8

    # Get the column names from the table
    columns_query = f"PRAGMA table_info(persoon_tab{table_version})"
    columns = [row[1] for row in conn.execute(columns_query).fetchall()]

    # Query the database for the person with the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM persoon_tab{table_version}
    WHERE rinpersoon = ?
    """
    
    # result = conn.execute(query, [rinpersoon]).fetchone() ## temp
    result = conn.execute(query, [rinpersoon]).fetchone()

    if not result:
        raise ValueError(f"No person found with rinpersoon {rinpersoon}")

    # Create a dictionary with column names as keys and row values as values
    person_row = dict(zip(columns, result))

    # Close the database connection
    # conn.close()

    # Create the PersonAttributesParagraph object
    person_attributes = PersonAttributesParagraph(
        dataset_name="persoon_tab" + table_version,
        rinpersoon=person_row['RINPERSOON'],
        GBAGEBOORTELAND=person_row['GBAGEBOORTELAND'],
        GBAGESLACHT=person_row['GBAGESLACHT'],
        GBAGEBOORTEJAAR=person_row['GBAGEBOORTEJAAR'],
        # GBAHERKOMSTGROEPEING=person_row['GBAHERKOMSTLAND'],
        # GBAGEBOORTELANDNL=person_row['GBAGEBOORTELANDNL'],
        GBAHERKOMSTGROEPERING=person_row['GBAHERKOMSTGROEPERING'],
        GBAGENERATIE=person_row['GBAGENERATIE'],
        GBAAANTALOUDERSBUITENLAND=person_row['GBAAANTALOUDERSBUITENLAND'],
        GBAGEBOORTELANDMOEDER=person_row['GBAGEBOORTELANDMOEDER'],
        GBAGESLACHTMOEDER=person_row['GBAGESLACHTMOEDER'],
        GBAGEBOORTEJAARMOEDER=person_row['GBAGEBOORTEJAARMOEDER'],
        GBAGEBOORTELANDVADER=person_row['GBAGEBOORTELANDVADER'],
        GBAGESLACHTVADER=person_row['GBAGESLACHTVADER'],
        GBAGEBOORTEJAARVADER=person_row['GBAGEBOORTEJAARVADER'],
    )

    return person_attributes

# Example usage
# db_path = 'synthetic_data.db'  # Replace with the path to your SQLite database
# person_id = '12345'  # Replace with the actual person_id you want to query
# person_attributes = get_person_attributes(person_id, db_path)
# print(person_attributes)