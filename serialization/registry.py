"""Registry mapping dataset names to their paragraph instantiator functions.

Each instantiator has the signature

    instantiator(rinpersoons, conn, table_version="", explicit=True, order=0)
        -> dict[str, list[Paragraph]]

and turns the rows of one data source into ``Paragraph`` objects keyed by
``rinpersoon``. To add support for a new data source, implement an instantiator
(see ``serialization/instantiator_scripts/``) and register it here. This is the
single place that needs editing to expose a new source to recipes; see the
"Extending BOLT: Adding New Data Sources" section of the README.
"""
from typing import Callable, Dict

from serialization.instantiator_scripts.persoon_tab import get_person_attributes
from serialization.instantiator_scripts.household_bus import get_households

# Base dataset name (the recipe ``name:`` with any ``table_version`` suffix
# removed) -> instantiator callable.
INSTANTIATORS: Dict[str, Callable] = {
    "persoon_tab": get_person_attributes,
    "household_bus": get_households,
}


def get_instantiator(dataset_name: str, table_version: str = "") -> Callable:
    """Return the instantiator registered for ``dataset_name``.

    Parameters
    ----------
    dataset_name : str
        The dataset name as written in a recipe (may include ``table_version``).
    table_version : str, default ""
        Optional suffix appended to table/dataset names.

    Raises
    ------
    ValueError
        If no instantiator is registered for the (de-versioned) dataset name.
    """
    base_name = dataset_name
    if table_version and dataset_name.endswith(table_version):
        base_name = dataset_name[: -len(table_version)]

    try:
        return INSTANTIATORS[base_name]
    except KeyError:
        raise ValueError(
            f"No instantiator registered for dataset '{dataset_name}'. "
            f"Registered datasets: {sorted(INSTANTIATORS)}. "
            f"To add a new source, implement an instantiator and register it in "
            f"serialization/registry.py (see 'Extending BOLT: Adding New Data "
            f"Sources' in the README)."
        )
