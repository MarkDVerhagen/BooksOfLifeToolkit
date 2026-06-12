from dataclasses import fields
from typing import Dict, List, Any
from serialization.instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph


def get_person_attributes(rinpersoons: list, conn, table_version: str = '', explicit: bool = True, order: int = 0) -> Dict[str, List[PersonAttributesParagraph]]:
    """Load personal attributes for the given ``rinpersoons`` from the database.

    Each database row is mapped to a :class:`PersonAttributesParagraph`. Columns
    are matched to dataclass fields *by name* (never by position), so the result
    is robust to differences in column ordering between the database schema and
    the dataclass definition.

    Parameters
    ----------
    rinpersoons : list[str]
        Identifiers to fetch.
    conn : duckdb.DuckDBPyConnection
        Open (read-only) connection containing the ``persoon_tab`` table.
    table_version : str, default ""
        Optional suffix appended to the table name (e.g. ``"_v1"``).
    explicit : bool, default True
        Whether the resulting paragraphs render every requested field.
    order : int, default 0
        Sort priority assigned to the resulting paragraphs.

    Returns
    -------
    dict[str, list[PersonAttributesParagraph]]
        Mapping from ``rinpersoon`` to its list of paragraphs (empty list when
        the person is absent from the table).
    """
    columns_query = f"PRAGMA table_info(persoon_tab{table_version})"
    columns = [row[1] for row in conn.execute(columns_query).fetchall()]

    query = f"""
    SELECT {', '.join(columns)} FROM persoon_tab{table_version}
    WHERE rinpersoon IN ({','.join('?' for _ in rinpersoons)})
    ORDER BY rinpersoon
    """
    results = conn.execute(query, tuple(rinpersoons)).fetchall()

    # Restrict to columns that map onto an actual paragraph field so extra
    # database columns do not raise a TypeError on construction.
    valid_fields = {f.name for f in fields(PersonAttributesParagraph)}

    grouped_results: Dict[str, List[Dict[str, Any]]] = {}
    for row in results:
        row_dict = dict(zip(columns, row))
        rinpersoon = row_dict['rinpersoon']
        grouped_results.setdefault(rinpersoon, []).append(row_dict)

    par_dict: Dict[str, List[PersonAttributesParagraph]] = {rinpersoon: [] for rinpersoon in rinpersoons}
    for rinpersoon in rinpersoons:
        for row_dict in grouped_results.get(rinpersoon, []):
            attrs = {
                key: value
                for key, value in row_dict.items()
                if key != 'rinpersoon' and key in valid_fields
            }
            par_dict[rinpersoon].append(PersonAttributesParagraph(
                dataset_name="persoon_tab",
                rinpersoon=rinpersoon,
                explicit=explicit,
                order=order,
                **attrs,
            ))

    return par_dict