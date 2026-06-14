from typing import Dict, List, Tuple

from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph

# CBS household-type (TYPHH) codes -> human-readable labels.
HOUSEHOLD_TYPES = {
    "1": "single-person",
    "2": "unmarried couple without children",
    "3": "married couple without children",
    "4": "unmarried couple with children",
    "5": "married couple with children",
    "6": "single parent",
    "7": "other",
}

# CBS place-in-household (PLHH) codes -> human-readable labels.
HOUSEHOLD_PLACES = {
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

# Which PLHH codes count as children / partners when classifying co-members of a
# household spell. Everything else is treated as an "other" member.
CHILD_PLACE_CODES = {"1"}
PARTNER_PLACE_CODES = {"3", "4", "5", "6"}


def classify_members(members: List[Tuple[str, str]], focal_rinpersoon: str):
    """Split co-members of a household spell into children, partners, and others.

    Parameters
    ----------
    members : list[tuple[str, str]]
        ``(rinpersoon, PLHH_code)`` for every person in the spell.
    focal_rinpersoon : str
        The person whose book is being written; excluded from the result.

    Returns
    -------
    tuple[list[str], list[str], list[str]]
        ``(children, partners, other_members)`` lists of rinpersoon identifiers.
    """
    children, partners, other = [], [], []
    for member_rinpersoon, place_code in members:
        if member_rinpersoon == focal_rinpersoon:
            continue
        if place_code in CHILD_PLACE_CODES:
            children.append(member_rinpersoon)
        elif place_code in PARTNER_PLACE_CODES:
            partners.append(member_rinpersoon)
        else:
            other.append(member_rinpersoon)
    return children, partners, other


def fill_household_par(rinpersoon, explicit, order, row_dict, dataset_name="household_bus",
                       children=None, partners=None, other_members=None):
    return HouseholdEventParagraph(
        dataset_name=dataset_name,
        explicit=explicit,
        order=order,
        rinpersoon=rinpersoon,
        HUISHOUDNR=row_dict['HUISHOUDNR'] if row_dict['HUISHOUDNR'] else 'nan',
        TYPHH=HOUSEHOLD_TYPES.get(row_dict['TYPHH'], "unknown type"),
        DATUMAANVANGHH=row_dict['DATUMAANVANGHH'],
        DATUMEINDEHH=row_dict['DATUMEINDEHH'],
        AANTALPERSHH=row_dict.get('AANTALPERSHH'),
        PLHH=HOUSEHOLD_PLACES.get(row_dict['PLHH'], "unknown place"),
        REFPERSOONHH="yes" if str(row_dict['REFPERSOONHH']) == "1" else "no",
        AANTALOVHH=row_dict['AANTALOVHH'] if str(row_dict['TYPHH']) != "1" else 'nan',
        AANTALKINDHH=row_dict['AANTALKINDHH'] if row_dict['AANTALKINDHH'] != "0" else 'nan',
        GEBJAARJONGSTEKINDHH=row_dict['GEBJAARJONGSTEKINDHH'].split('.')[0],
        GEBMAANDJONGSTEKINDHH=row_dict['GEBMAANDJONGSTEKINDHH'].split('.')[0],
        GEBJAAROUDSTEKINDHH=row_dict['GEBJAAROUDSTEKINDHH'].split('.')[0],
        GEBMAANDOUDSTEKINDHH=row_dict['GEBMAANDOUDSTEKINDHH'].split('.')[0],
        CHILDREN=children if children is not None else [],
        PARTNERS=partners if partners is not None else [],
        OTHER_MEMBERS=other_members if other_members is not None else [],
    )


def _build_spell_membership(conn, table_version, household_ids) -> Dict[Tuple[str, str], List[Tuple[str, str]]]:
    """Map each household spell to the people who share it.

    A spell is identified by ``(HUISHOUDNR, DATUMAANVANGHH)``. This powers the
    "who" of a book of life: the other people present in a focal person's
    household at a given time (the social context).
    """
    membership: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
    if not household_ids:
        return membership

    placeholders = ','.join('?' for _ in household_ids)
    member_query = f"""
    SELECT rinpersoon, HUISHOUDNR, DATUMAANVANGHH, PLHH
    FROM household_bus{table_version}
    WHERE HUISHOUDNR IN ({placeholders})
    """
    for member_rinpersoon, hh_id, start_date, place_code in conn.execute(member_query, tuple(household_ids)).fetchall():
        membership.setdefault((hh_id, start_date), []).append((member_rinpersoon, place_code))
    return membership


def get_households(rinpersoons, conn, table_version: str = '', explicit: bool = True, order: int = 0) -> Dict[str, List[HouseholdEventParagraph]]:
    """Load household spells for ``rinpersoons`` and attach their social context.

    For every household spell of a focal person, the other members of that spell
    are discovered and classified into children, partners, and other members
    (the "who" of a book of life). Members are matched to dataclass fields by
    name, and the result is keyed by ``rinpersoon`` (empty list when absent).
    """
    columns_query = f"PRAGMA table_info(household_bus{table_version})"
    columns = [row[1] for row in conn.execute(columns_query).fetchall()]

    query = f"""
    SELECT {', '.join(columns)} FROM household_bus{table_version}
    WHERE rinpersoon IN ({','.join('?' for _ in rinpersoons)})
    ORDER BY rinpersoon
    """
    results = conn.execute(query, tuple(rinpersoons)).fetchall()

    grouped_results: Dict[str, List[dict]] = {}
    household_ids = set()
    for row in results:
        row_dict = dict(zip(columns, row))
        rinpersoon = row_dict['rinpersoon']
        grouped_results.setdefault(rinpersoon, []).append(row_dict)
        household_ids.add(row_dict['HUISHOUDNR'])

    # Resolve the co-members of every spell touched by the focal persons.
    membership = _build_spell_membership(conn, table_version, list(household_ids))

    par_dict: Dict[str, List[HouseholdEventParagraph]] = {rinpersoon: [] for rinpersoon in rinpersoons}
    for rinpersoon in rinpersoons:
        for row_dict in grouped_results.get(rinpersoon, []):
            spell_key = (row_dict['HUISHOUDNR'], row_dict['DATUMAANVANGHH'])
            children, partners, other = classify_members(
                membership.get(spell_key, []), rinpersoon
            )
            par_dict[rinpersoon].append(fill_household_par(
                rinpersoon=rinpersoon,
                explicit=explicit,
                order=order,
                row_dict=row_dict,
                children=children,
                partners=partners,
                other_members=other,
            ))

    return par_dict
