import duckdb
import re
import json
import numpy as np
from typing import List
from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph

# def get_households(rinpersoon: str, db_name: str = 'synthetic_data.duckdb', table_version: str = '') -> List[HouseholdEventParagraph]: ## 20/8
def get_households(rinpersoon: str, conn, table_version: str = '') -> List[HouseholdEventParagraph]: ## 20/8
    """
    This function loads all households for a given rinpersoon (person_id)
    by querying the SQLite database and creating a list of HouseholdEventParagraph objects.
    """
    # Connect to the database
    # conn = duckdb.connect(db_name, read_only=True) ## 20/8

    # Get the column names from the table
    columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'household_bus{table_version}'"
    columns = [row[0] for row in conn.execute(columns_query).fetchall()]

    # Query the database for all households related to the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM household_bus{table_version}
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
        
        household_types = {
                "1": "single-person",
                "2": "unmarried couple without children",
                "3": "married couple without children",
                "4": "unmarried couple with children",
                "5": "married couple with children",
                "6": "single parent",
                "7": "other"
            }
        
        household_places = {
                "1": "child",
                "2": "single-person",
                "3": "partner",
                "4": "partner",
                "5": "partner",
                "6": "partner",
                "7": "single-parent",
                "8": "other",
                "9": "other",
                "10": "institutional",
            }

        household_paragraph = HouseholdEventParagraph(
            dataset_name="household_bus" + table_version,
            rinpersoon=rinpersoon,
            HUISHOUDNR=row_dict['HUISHOUDNR'],
            TYPHH=household_types.get(row_dict['TYPHH'], "unknown type"),
            DATUMAANVANGHH=row_dict['DATUMAANVANGHH'],
            DATUMEINDEHH=row_dict['DATUMEINDEHH'],
            AANTALPERSHH=row_dict['AANTALPERSHH'],
            PLHH=household_places.get(row_dict['PLHH'], "unknown place"),
            REFPERSOONHH=row_dict['REFPERSOONHH'],
            AANTALOVHH=row_dict['AANTALOVHH'],
            AANTALKINDHH=row_dict['AANTALKINDHH'],
            CHILDREN = ', '.join([re.sub(r'.*\[|\].*', '', i) for i in [row_dict['ID_list_1']] if i != "nan"]),
            PARTNERS= ', '.join([re.sub(r'.*\[|\].*', '', i) for i in [row_dict['ID_list_3'], row_dict['ID_list_4'], row_dict['ID_list_5'], row_dict['ID_list_6']] if i != "nan"]),
            OTHER_MEMBERS=', '.join([re.sub(r'.*\[|\].*', '', i) for i in [row_dict['ID_list_2'], row_dict['ID_list_7'], row_dict['ID_list_8'], row_dict['ID_list_9'], row_dict['ID_list_10']] if i != "nan"]),
            GEBJAARJONGSTEKINDHH=row_dict['GEBJAARJONGSTEKINDHH'].split('.')[0],
            GEBMAANDJONGSTEKINDHH=row_dict['GEBMAANDJONGSTEKINDHH'].split('.')[0],
            GEBJAAROUDSTEKINDHH=row_dict['GEBJAAROUDSTEKINDHH'].split('.')[0],
            GEBMAANDOUDSTEKINDHH=row_dict['GEBMAANDOUDSTEKINDHH'].split('.')[0],
            
        )
        household_paragraphs.append(household_paragraph)

    # Close the database connection
    # conn.close() ## 20/8

    return household_paragraphs

