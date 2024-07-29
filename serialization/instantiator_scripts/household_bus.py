import duckdb
import json
from typing import List
from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph

def get_households(rinpersoon: str, db_name: str = 'synthetic_data.duckdb') -> List[HouseholdEventParagraph]:
    """
    This function loads all households for a given rinpersoon (person_id)
    by querying the SQLite database and creating a list of HouseholdEventParagraph objects.
    """
    # Connect to the database
    conn = duckdb.connect(db_name, read_only=True)

    # Get the column names from the table
    columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'household_bus'"
    columns = [row[0] for row in conn.execute(columns_query).fetchall()]

    # Query the database for all households related to the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM household_bus
    WHERE rinpersoon = ?
    """
    results = conn.execute(query, [rinpersoon]).fetchall()

    # Create a list to hold HouseholdEventParagraph objects
    household_paragraphs = []

    # Iterate over each row to create HouseholdEventParagraph objects
    for row in results:
        # Convert row to a dictionary
        row_dict = dict(zip(columns, row))

        # TODO Replace this for loop with the actual istantiation of the hoousehold mmebers from edited table
        # Parse JSON strings for specific fields if they exist
        for field in ['CHILDREN', 'PARTNERS', 'OTHER_MEMBERS', 'ALL_MEMBERS']:
            if row_dict.get(field):
                try:
                    row_dict[field] = json.loads(row_dict[field])
                except json.JSONDecodeError:
                    # If it's not valid JSON, keep it as is
                    pass

        household_paragraph = HouseholdEventParagraph(
            dataset_name="household_bus",
            rinpersoon=rinpersoon,
            HOUSEKEEPING_NR=row_dict['HOUSEKEEPING_NR'],
            TYPHH=row_dict['TYPHH'],
            DATE_STIRTHH=row_dict['DATE_STIRTHH'],
            DATUMEINDEHH=row_dict['DATUMEINDEHH'],
            NUMBERPERSHH=int(row_dict['NUMBERPERSHH']),
            PLHH=row_dict['PLHH'],
            REFPERSOONHH=row_dict['REFPERSOONHH'],
            AANTALOVHH=int(row_dict['AANTALOVHH']),
            AANTALKINDHH=int(row_dict['AANTALKINDHH']),
            BIRTHEDYOUNGCHILDHH=row_dict['BIRTHEDYOUNGCHILDHH'],
            GEBMAANDJONGSTEKINDHH=row_dict['GEBMAANDJONGSTEKINDHH'],
            GEBJAAROUDSTEKINDHH=row_dict['GEBJAAROUDSTEKINDHH'],
            BMAANDOUDSTEKINDHH=row_dict['BMAANDOUDSTEKINDHH'],
            CHILDREN=["00a2cd32", "00a2cd32"], # TODO remove this hardcoded value
            PARTNERS=["00a2cd32", "00a2cd32"],
            OTHER_MEMBERS=row_dict.get('OTHER_MEMBERS'),
            ALL_MEMBERS=row_dict.get('ALL_MEMBERS')
        )
        household_paragraphs.append(household_paragraph)

    # Close the database connection
    conn.close()

    return household_paragraphs

