import duckdb
from typing import Dict, Any
from serialization.instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph

def get_person_attributes(rinpersoon: str, db_name: str = 'synthetic_data.duckdb') -> PersonAttributesParagraph:
    """
    This function loads personal attributes for a given rinpersoon (person_id)
    by querying the SQLite database and creating the PersonAttributesParagraph object.
    """
   # Connect to the database
    conn = duckdb.connect(db_name, read_only=True)

    # Get the column names from the table
    columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'persoon_tab'"
    columns = [row[0] for row in conn.execute(columns_query).fetchall()]

    # Query the database for the person with the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM persoon_tab
    WHERE rinpersoon = ?
    """
    result = conn.execute(query, [rinpersoon]).fetchone()

    if not result:
        raise ValueError(f"No person found with rinpersoon {rinpersoon}")

    # Create a dictionary with column names as keys and row values as values
    person_row = dict(zip(columns, result))

    # Close the database connection
    conn.close()

    # Create the PersonAttributesParagraph object
    person_attributes = PersonAttributesParagraph(
        dataset_name="persoon_tab",
        rinpersoon=person_row['rinpersoon'],
        GBAGEBOORTELAND=person_row['GBAGEBOORTELAND'],
        GBAGESLACHT=person_row['GBAGESLACHT'],
        GBAGEBOORTEJAAR=int(person_row['GBAGEBOORTEJAAR']),
        GBAHERKOMSTLAND=person_row['GBAHERKOMSTLAND'],
        GBAGEBOORTELANDNL=person_row['GBAGEBOORTELANDNL'],
        GBAHERKOMSTGROEPERING=person_row['GBAHERKOMSTGROEPERING'],
        GBAGENERATIE=person_row['GBAGENERATIE'],
        GBAAANTALOUDERSBUITENLAND=int(person_row['GBAAANTALOUDERSBUITENLAND']),
        GBAGEBOORTELANDMOEDER=person_row['GBAGEBOORTELANDMOEDER'],
        GBAGESLACHTMOEDER=person_row['GBAGESLACHTMOEDER'],
        GBAGEBOORTEJAARMOEDER=int(person_row['GBAGEBOORTEJAARMOEDER']),
        GBAGEBOORTELANDVADER=person_row['GBAGEBOORTELANDVADER'],
        GBAGESLACHTVADER=person_row['GBAGESLACHTVADER'],
        GBAGEBOORTEJAARVADER=int(person_row['GBAGEBOORTEJAARVADER']),
    )

    return person_attributes

# Example usage
# db_path = 'synthetic_data.db'  # Replace with the path to your SQLite database
# person_id = '12345'  # Replace with the actual person_id you want to query
# person_attributes = get_person_attributes(person_id, db_path)
# print(person_attributes)