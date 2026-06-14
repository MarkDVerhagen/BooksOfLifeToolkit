
from itertools import chain

from serialization.Recipe import Recipe
from serialization.registry import get_instantiator

class BookofLifeGeneratorBatch:
    def __init__(self, rinpersoons, recipe_yaml_path, db_path, duck_db_conn, table_version=""):
        self.rinpersoons = rinpersoons
        self.recipe = Recipe(recipe_yaml_path)
        self.book: str = ""
        self.paragraphs_dict_list = []
        self.db_path = db_path
        self.table_version = table_version
        self.conn = duck_db_conn
        self.instantiate_paragraph_dicts()

    def instantiate_paragraph_dicts(self):
        for dataset in self.recipe.datasets:
            dataset_name = dataset.get('name')
            explicit = dataset.get('explicit', False)
            order = dataset.get('sort_key', 0)

            instantiator = get_instantiator(dataset_name, self.table_version)
            self.paragraphs_dict_list.append(
                instantiator(self.rinpersoons, self.conn, self.table_version, explicit, order)
            )
    
    def combine_paragraphs(self, dict_list):
        combined_dict = {}

        for key in dict_list[0]:
            combined_dict[key] = []
            combined_dict[key] = list(chain(*[d[key] for d in dict_list]))
        return combined_dict

    def write_books(self):
        """Combine the per-source paragraph dicts into one dict keyed by rinpersoon."""
        self.rin_dicts = self.combine_paragraphs(self.paragraphs_dict_list)