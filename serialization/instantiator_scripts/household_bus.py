import sqlite3
import json
from typing import List
from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph

def get_households(rinpersoon: str, db_path: str = 'synthetic_data.db') -> List[HouseholdEventParagraph]:
    """
    This function loads all households for a given rinpersoon (person_id)
    by querying the SQLite database and creating a list of HouseholdEventParagraph objects.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()

    # Query the database for all households related to the given rinpersoon
    query = """
    SELECT * FROM household_bus
    WHERE rinpersoon = ?
    """
    cursor.execute(query, (rinpersoon,))
    results = cursor.fetchall()

    # Create a list to hold HouseholdEventParagraph objects
    household_paragraphs = []

    # Iterate over each row to create HouseholdEventParagraph objects
    for row in results:
        # Convert sqlite3.Row object to a regular dictionary
        row_dict = dict(row)

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
            CHILDREN=row_dict.get('CHILDREN'),
            PARTNERS=row_dict.get('PARTNERS'),
            OTHER_MEMBERS=row_dict.get('OTHER_MEMBERS'),
            ALL_MEMBERS=row_dict.get('ALL_MEMBERS')
        )
        household_paragraphs.append(household_paragraph)

    # Close the database connection
    conn.close()

    return household_paragraphs

