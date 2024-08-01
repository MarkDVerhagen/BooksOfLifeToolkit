import duckdb
import json
from typing import List
from serialization.instantiator_scripts.EducationEventParagraph import EducationEventParagraph

def get_education_events(rinpersoon: str, db_name: str = 'synthetic_data.duckdb') -> List[EducationEventParagraph]:
    # Connect to the database
    conn = duckdb.connect(db_name, read_only=True)

    # Get the column names from the table
    columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'education_bus'"
    columns = [row[0] for row in conn.execute(columns_query).fetchall()]

    query = f"""
    SELECT {', '.join(columns)} FROM education_bus
    WHERE rinpersoon = ?
    """
    results = conn.execute(query, [rinpersoon]).fetchall()

    # Create a list to hold EducationEventParagraph objects
    education_paragraphs = []

    # Iterate over each row to create EducationEventParagraph objects
    for row in results:
        # Convert row to a dictionary
        row_dict = dict(zip(columns, row))

        education_paragraph = EducationEventParagraph(
            dataset_name="education_bus",
            rinpersoon=rinpersoon,
            year = int(row_dict['year']) if 'year' in row_dict else None,
            OPLNRHB=row_dict['OPLNRHB'] if 'OPLNRHB' in row_dict else None,
            OPLNRHG=row_dict['OPLNRHG'] if 'OPLNRHG' in row_dict else None,
            OPLNIVSOI2016AGG4HBMETNIRWO=row_dict['OPLNIVSOI2016AGG4HBMETNIRWO'] if 'OPLNIVSOI2016AGG4HBMETNIRWO' in row_dict else None,
            OPLNIVSOI2016AGG4HGMETNIRWO=row_dict['OPLNIVSOI2016AGG4HGMETNIRWO'] if 'OPLNIVSOI2016AGG4HGMETNIRWO' in row_dict else None,
            RICHTdetailISCEDF2013HBmetNIRWO=row_dict['RICHTdetailISCEDF2013HBmetNIRWO'] if 'RICHTdetailISCEDF2013HBmetNIRWO' in row_dict else None,
            RICHTdetailISCEDF2013HGmetNIRWO=row_dict['RICHTdetailISCEDF2013HGmetNIRWO'] if 'RICHTdetailISCEDF2013HGmetNIRWO' in row_dict else None,
            OPLNIVSOI2021AGG4HBmetNIRWO=row_dict['OPLNIVSOI2021AGG4HBmetNIRWO'] if 'OPLNIVSOI2021AGG4HBmetNIRWO' in row_dict else None,
            OPLNIVSOI2021AGG4HGmetNIRWO=row_dict['OPLNIVSOI2021AGG4HGmetNIRWO'] if 'OPLNIVSOI2021AGG4HGmetNIRWO' in row_dict else None,
            RICHTSOI2021SCEDF2013HBNIRWO=row_dict['RICHTSOI2021SCEDF2013HBNIRWO'] if 'RICHTSOI2021SCEDF2013HBNIRWO' in row_dict else None,
            RICHTSOI2021SCEDF2013HGNIRWO=row_dict['RICHTSOI2021SCEDF2013HGNIRWO'] if 'RICHTSOI2021SCEDF2013HGNIRWO' in row_dict else None
        )
        education_paragraphs.append(education_paragraph)

    # Close the database connection
    conn.close()

    return education_paragraphs

