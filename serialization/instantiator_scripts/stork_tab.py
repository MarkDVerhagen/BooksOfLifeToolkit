import duckdb
import sqlite3
from typing import Dict, Any
from serialization.instantiator_scripts.StorkParagraph import StorkParagraph

# def get_person_attributes(rinpersoon: str, db_name: str = 'synthetic_data.duckdb', table_version: str = '') -> PersonLocationParagraph: ## 20/8
def get_stork(rinpersoons: list, conn, table_version: str = '', explicit : bool=True, order: int = 0) -> StorkParagraph: ## 20/8
    """
    This function loads personal attributes for a given rinpersoon (person_id)
    by querying the SQLite database and creating the StorkParagraph object.
    """
    # conn = duckdb.connect(db_name, read_only=True) ## 20/8

    columns_query = f"PRAGMA table_info(stork_tab{table_version})"
    columns = [row[1] for row in conn.execute(columns_query).fetchall()]

    # Query the database for the person with the given rinpersoon
    query = f"""
    SELECT {', '.join(columns)} FROM stork_tab{table_version}
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
        par_dict[rinpersoon] = [StorkParagraph(
            dataset_name="stork_tab",
            rinpersoon=rinpersoon,
            explicit=explicit, order=order,
            **dict(zip(columns, result))) for result in grouped_results[rinpersoon]]

    return par_dict