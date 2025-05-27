import duckdb
import re
import json
import numpy as np
from typing import List
from serialization.instantiator_scripts.MovingEventParagraph import MovingEventParagraph

# def get_objects(rinpersoon: str, db_name: str = 'synthetic_data.duckdb', table_version: str = '') -> List[MovingEventParagraph]: ## 20/8
def get_objects(rinpersoons: list, conn, table_version: str = '', explicit: bool = True, order: int = 0) -> List[MovingEventParagraph]: ## 20/8
    """
    This function loads all objects for a given rinpersoon (person_id)
    by querying the SQLite database and creating a list of MovingEventParagraph objects.
    """
    # Connect to the database
    # conn = duckdb.connect(db_name, read_only=True) ## 20/8

    # Get the column names from the table
    columns_query = f"PRAGMA table_info(object_bus{table_version})"
    columns = [row[1] for row in conn.execute(columns_query).fetchall()]

    # Query the database for the person with the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM object_bus{table_version}
    WHERE rinpersoon IN ({','.join('?' for _ in rinpersoons)})
    ORDER BY rinpersoon
    """

    # result = conn.execute(query, [rinpersoon]).fetchone() ## temp
    results = conn.execute(query, tuple(rinpersoons)).fetchall()

    grouped_results = {}

    for row in results:
        rinpersoon = row[columns.index('RINPERSOON')]
        row_list = list(row)
        rinpersoon_index = columns.index('RINPERSOON')
        del row_list[rinpersoon_index]
        if rinpersoon not in grouped_results:
            grouped_results[rinpersoon] = []
        grouped_results[rinpersoon].append(row)

    columns = [c for c in columns if c != "RINPERSOON"]
    par_dict = {}
    for rinpersoon in rinpersoons:
        par_dict[rinpersoon] = [MovingEventParagraph(
            dataset_name="object_bus",
            rinpersoon=rinpersoon,
            explicit=explicit, order=order,
            **dict(zip(columns, result))) for result in grouped_results[rinpersoon]]

    # Close the database connection
    # conn.close() ## 20/8

    return par_dict

