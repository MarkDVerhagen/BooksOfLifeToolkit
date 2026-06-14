"""Tests for the core book-of-life generation paths.

Several of these are regression tests for bugs that produced silently-wrong
books (person attributes shifted by one column, household codes not mapped,
"last N spells" keeping the wrong spells, reference-person always "no").
"""
import pytest

from serialization.BookofLifeGenerator import BookofLifeGenerator
from serialization.instantiator_scripts.persoon_tab import get_person_attributes
from serialization.instantiator_scripts.household_bus import get_households
from serialization.registry import get_instantiator


def _recipe(datasets, sorting_keys=("year",)):
    return {
        "main_key": "rinpersoon",
        "datasets": datasets,
        "formatting": {
            "sorting_keys": list(sorting_keys),
            "paragraph_generator": "get_paragraph_string_tabular",
        },
    }


def test_person_attributes_not_shifted(conn):
    """Regression: person fields must map by name, not be shifted by one column."""
    pars = get_person_attributes(["p1"], conn)["p1"]
    assert len(pars) == 1
    par = pars[0]
    assert par.GBAGEBOORTEJAAR == "1980"
    assert par.GBAGESLACHT == "1"
    assert par.GBAGEBOORTEJAARVADER == "1950"


def test_person_tabular_render_shows_correct_year(conn):
    pars = get_person_attributes(["p1"], conn, explicit=False)["p1"]
    rendered = pars[0].get_paragraph_string_tabular(["GBAGEBOORTEJAAR"])
    assert "Year of Birth: 1980" in rendered


def test_household_codes_are_mapped(conn):
    """Numeric TYPHH/PLHH codes must resolve to labels, not 'unknown'."""
    pars = get_households(["p1"], conn)["p1"]
    types = {p.TYPHH for p in pars}
    assert "married couple with children" in types
    assert "single-person" in types
    assert "unknown type" not in types
    assert all(p.PLHH != "unknown place" for p in pars)


def test_reference_person_flag(conn):
    """Regression: REFPERSOONHH '1' (string) must render as 'yes'."""
    pars = get_households(["p1"], conn)["p1"]
    assert all(p.REFPERSOONHH == "yes" for p in pars)


def test_social_context_members_classified(conn):
    """The 'who': co-members are split into partners/children correctly."""
    pars = get_households(["p1"], conn)["p1"]
    spell_a = next(p for p in pars if p.HUISHOUDNR == "HH1")
    assert spell_a.PARTNERS == ["p2"]
    assert spell_a.CHILDREN == ["c1"]
    assert spell_a.OTHER_MEMBERS == []


def test_absent_person_returns_empty_list(conn):
    assert get_person_attributes(["does_not_exist"], conn)["does_not_exist"] == []


def test_n_spell_keeps_most_recent(conn):
    """Regression: n_spell must keep the LAST n spells, not drop the first n."""
    recipe = _recipe([{"name": "household_bus", "features": ["HUISHOUDNR"], "n_spell": 1}])
    book = BookofLifeGenerator("p1", recipe, duck_db_conn=conn).generate_book()
    assert "HH2" in book  # most recent spell kept
    assert "HH1" not in book  # older spell dropped


def test_books_within_books(conn):
    """Social-context recipe embeds a sub-book for the partner."""
    recipe = _recipe(
        [
            {
                "name": "household_bus",
                "features": ["HUISHOUDNR", "TYPHH"],
                "social_context_features": {
                    "PARTNERS": [{"name": "persoon_tab", "features": ["GBAGEBOORTEJAAR"]}]
                },
            }
        ]
    )
    book = BookofLifeGenerator("p1", recipe, duck_db_conn=conn).generate_book()
    assert "[PARTNERS p2]" in book
    assert "Year of Birth: 1982" in book  # the partner's birth year


def test_social_depth_zero_disables_subbooks(conn):
    recipe = _recipe(
        [
            {
                "name": "household_bus",
                "features": ["HUISHOUDNR"],
                "social_context_features": {
                    "PARTNERS": [{"name": "persoon_tab", "features": ["GBAGEBOORTEJAAR"]}]
                },
            }
        ]
    )
    book = BookofLifeGenerator("p1", recipe, duck_db_conn=conn, social_depth=0).generate_book()
    assert "[PARTNERS" not in book


def test_full_book_generation(conn):
    recipe = _recipe(
        [
            {"name": "persoon_tab", "features": ["GBAGEBOORTEJAAR", "GBAGESLACHT"]},
            {"name": "household_bus", "features": ["HUISHOUDNR", "TYPHH", "PLHH"]},
        ]
    )
    book = BookofLifeGenerator("p1", recipe, duck_db_conn=conn).generate_book()
    assert "Year of Birth: 1980" in book
    assert "married couple with children" in book


def test_registry_known_datasets():
    assert get_instantiator("persoon_tab") is not None
    assert get_instantiator("household_bus") is not None


def test_registry_unknown_dataset_raises():
    with pytest.raises(ValueError, match="No instantiator registered"):
        get_instantiator("employment_bus")
