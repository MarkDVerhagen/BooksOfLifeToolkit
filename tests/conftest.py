"""Shared fixtures: a tiny, fully-known DuckDB database.

The database mirrors the schema produced by ``serialization/make_db.py`` (every
column stored as VARCHAR) so the tests exercise the real instantiator code paths
against values we control exactly.
"""
import duckdb
import pandas as pd
import pytest

# Focal person p1 lives with partner p2 and child c1 (spell A), then alone (spell B).
PERSOON_TAB = pd.DataFrame(
    [
        # rinpersoon, country, gender, birth year, father gender, father birth year
        {"rinpersoon": "p1", "GBAGEBOORTELAND": "NL", "GBAGESLACHT": "1", "GBAGEBOORTEJAAR": "1980", "GBAGESLACHTVADER": "1", "GBAGEBOORTEJAARVADER": "1950"},
        {"rinpersoon": "p2", "GBAGEBOORTELAND": "NL", "GBAGESLACHT": "2", "GBAGEBOORTEJAAR": "1982", "GBAGESLACHTVADER": "1", "GBAGEBOORTEJAARVADER": "1951"},
        {"rinpersoon": "c1", "GBAGEBOORTELAND": "NL", "GBAGESLACHT": "1", "GBAGEBOORTEJAAR": "2010", "GBAGESLACHTVADER": "1", "GBAGEBOORTEJAARVADER": "1980"},
    ]
)


def _household_row(rinpersoon, hh, typ, plhh, ref, start, end, npers, nov, nkind, has_children):
    return {
        "rinpersoon": rinpersoon,
        "HUISHOUDNR": hh,
        "TYPHH": typ,
        "PLHH": plhh,
        "REFPERSOONHH": ref,
        "DATUMAANVANGHH": start,
        "DATUMEINDEHH": end,
        "AANTALPERSHH": npers,
        "AANTALOVHH": nov,
        "AANTALKINDHH": nkind,
        "GEBJAARJONGSTEKINDHH": "2010" if has_children else "nan",
        "GEBMAANDJONGSTEKINDHH": "01" if has_children else "nan",
        "GEBJAAROUDSTEKINDHH": "2010" if has_children else "nan",
        "GEBMAANDOUDSTEKINDHH": "01" if has_children else "nan",
    }


HOUSEHOLD_BUS = pd.DataFrame(
    [
        # Spell A: married couple with children (TYPHH 5); p1 & p2 partners (4), c1 child (1).
        _household_row("p1", "HH1", "5", "4", "1", "19900101", "20000101", "3", "2", "1", True),
        _household_row("p2", "HH1", "5", "4", "0", "19900101", "20000101", "3", "2", "1", True),
        _household_row("c1", "HH1", "5", "1", "0", "19900101", "20000101", "3", "2", "1", True),
        # Spell B: p1 lives alone afterwards (single-person, TYPHH 1).
        _household_row("p1", "HH2", "1", "2", "1", "20000101", "20500101", "1", "0", "0", False),
    ]
)


@pytest.fixture
def conn(tmp_path):
    """A DuckDB connection to a freshly built, fully-known toy database."""
    db_path = str(tmp_path / "test.duckdb")
    connection = duckdb.connect(db_path)
    connection.register("persoon_df", PERSOON_TAB)
    connection.register("household_df", HOUSEHOLD_BUS)
    connection.execute("CREATE TABLE persoon_tab AS SELECT * FROM persoon_df")
    connection.execute("CREATE TABLE household_bus AS SELECT * FROM household_df")
    connection.unregister("persoon_df")
    connection.unregister("household_df")
    yield connection
    connection.close()
