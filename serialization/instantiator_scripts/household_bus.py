import duckdb
import re
import json
import numpy as np
from typing import List
from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph

def fill_household_par(rinpersoon, explicit, order, row_dict, dataset_name="household_bus"):
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
    return HouseholdEventParagraph(
        dataset_name=dataset_name,
        explicit=explicit,
        order=order,
        rinpersoon=rinpersoon,
        # HUISHOUDNR=row_dict['HUISHOUDNR'] if row_dict['HUISHOUDNR'] else 'nan',
        TYPHH=household_types.get(row_dict['TYPHH'], "unknown type"),
        DATUMAANVANGHH=row_dict['DATUMAANVANGHH'],
        DATUMEINDEHH=row_dict['DATUMEINDEHH'],
        AANTALPERSHH=row_dict['AANTALPERSHH'],
        PLHH=household_places.get(row_dict['PLHH'], "unknown place"),
        REFPERSOONHH= "yes" if (row_dict['REFPERSOONHH'] == 1) else "no",
        AANTALOVHH=row_dict['AANTALOVHH'] if row_dict['TYPHH'] != 1 else 'nan',
        AANTALKINDHH=row_dict['AANTALKINDHH'] if row_dict['AANTALKINDHH'] != "0" else 'nan',
        GEBJAARJONGSTEKINDHH=row_dict['GEBJAARJONGSTEKINDHH'].split('.')[0],
        GEBMAANDJONGSTEKINDHH=row_dict['GEBMAANDJONGSTEKINDHH'].split('.')[0],
        GEBJAAROUDSTEKINDHH=row_dict['GEBJAAROUDSTEKINDHH'].split('.')[0],
        GEBMAANDOUDSTEKINDHH=row_dict['GEBMAANDOUDSTEKINDHH'].split('.')[0],
        )


# def get_households(rinpersoon: str, db_name: str = 'synthetic_data.duckdb', table_version: str = '') -> List[HouseholdEventParagraph]: ## 20/8
def get_households(rinpersoons: str, conn, table_version: str = '', explicit: bool = True, order: int = 0) -> List[HouseholdEventParagraph]: ## 20/8
    """
    This function loads all households for a given rinpersoon (person_id)
    by querying the SQLite database and creating a list of HouseholdEventParagraph objects.
    """
    # Connect to the database
    # conn = duckdb.connect(db_name, read_only=True) ## 20/8

    columns_query = f"PRAGMA table_info(household_bus{table_version})"
    columns = [row[1] for row in conn.execute(columns_query).fetchall()]
    # columns = [c for c in columns if c != "RINPERSOON"]

    # Query the database for the person with the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM household_bus{table_version}
    WHERE rinpersoon IN ({','.join('?' for _ in rinpersoons)})
    ORDER BY rinpersoon
    """

    # result = conn.execute(query, [rinpersoon]).fetchone() ## temp
    results = conn.execute(query, tuple(rinpersoons)).fetchall()

    grouped_results = {}

    for row in results:
        rinpersoon = row[columns.index('RINPERSOON')]
        if rinpersoon not in grouped_results:
            grouped_results[rinpersoon] = []
        grouped_results[rinpersoon].append(row)

    par_dict = {}
    for rinpersoon in rinpersoons:
        par_dict[rinpersoon] = [fill_household_par(
            rinpersoon=rinpersoon,
            explicit=explicit, order=order,
            row_dict=dict(zip(columns, result))) for result in grouped_results[rinpersoon]]
    
        # # children_list = [re.sub(r'.*\[|\].*', '', i) for i in [row_dict['ID_list_1']] if i != "nan"] if row_dict['ID_list_1'] else 'nan'
        # # CHILDREN = ', '.join(children_list),
        # # PARTNERS= ', '.join([re.sub(r'.*\[|\].*', '', i) for i in [row_dict['ID_list_3'], row_dict['ID_list_4'], row_dict['ID_list_5'], row_dict['ID_list_6']] if i != "nan"]),
        # # OTHER_MEMBERS=', '.join([re.sub(r'.*\[|\].*', '', i) for i in [row_dict['ID_list_2'], row_dict['ID_list_7'], row_dict['ID_list_8'], row_dict['ID_list_9'], row_dict['ID_list_10']] if i != "nan"]),
        # household_paragraphs.append(household_paragraph)

    # Close the database connection
    # conn.close() ## 20/8

    return par_dict

