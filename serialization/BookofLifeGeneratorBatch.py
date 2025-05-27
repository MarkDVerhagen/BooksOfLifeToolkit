
from typing import List
from serialization.instantiator_scripts.Paragraph import Paragraph
from serialization.instantiator_scripts.PersonAttributesParagraph import PersonAttributesParagraph
from serialization.instantiator_scripts.LisaAttributesParagraph import LisaAttributesParagraph
from serialization.instantiator_scripts.HouseholdEventParagraph import HouseholdEventParagraph
from serialization.Recipe import Recipe
from serialization.instantiator_scripts.persoon_tab import get_person_attributes
from serialization.instantiator_scripts.lisa_tab import get_lisa_attributes
from serialization.instantiator_scripts.loc_lisa_tab import get_lisa_loc
from serialization.instantiator_scripts.wealth_lisa_tab import get_lisa_wealth
from serialization.instantiator_scripts.par_lisa_tab import get_lisa_par
from serialization.instantiator_scripts.inc_lisa_tab import get_lisa_inc
from serialization.instantiator_scripts.household_bus import get_households, fill_household_par
from serialization.instantiator_scripts.education_bus import get_education_events
from serialization.instantiator_scripts.employment_bus import get_employment_events
from serialization.instantiator_scripts.object_bus import get_objects
from serialization.instantiator_scripts.stork_tab import get_stork
from serialization.instantiator_scripts.stork2_tab import get_stork2
from operator import attrgetter
from itertools import chain
import duckdb

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
        # self.write_books()
        
        # self.social_context_paragraphs = self.instantiate_social_context_paragraphs(self.recipe.social_context_features)

    def instantiate_paragraph_dicts(self):
        for dataset in self.recipe.datasets:
            dataset_name = dataset.get('name')
            features = self.recipe.get_features(dataset_name)

            if dataset_name == 'persoon_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_person_attributes(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'lisa_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_lisa_attributes(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'loc_lisa_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_lisa_loc(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'wealth_lisa_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_lisa_wealth(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'inc_lisa_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_lisa_inc(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'par_lisa_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_lisa_par(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'household_bus' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_households(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'education_bus' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_education_events(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'employment_bus' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_employment_events(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'object_bus' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_objects(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'stork_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_stork(self.rinpersoons, self.conn, self.table_version, explicit, order))
            elif dataset_name == 'stork2_tab' + self.table_version:
                explicit = dataset.get('explicit', False)
                order = dataset.get('sort_key', 0)
                self.paragraphs_dict_list.append(get_stork2(self.rinpersoons, self.conn, self.table_version, explicit, order))
            else:
                raise ValueError(f"Dataset name {dataset_name + self.table_version} not recognized")
    
    def combine_paragraphs(self, dict_list):
        combined_dict = {}

        for key in dict_list[0]:
            combined_dict[key] = []
            combined_dict[key] = list(chain(*[d[key] for d in dict_list]))
        return combined_dict

    def write_books(self):
        self.rin_dicts = self.combine_paragraphs(self.paragraphs_dict_list)
        # for rinpersoon, paragraphs in batch_generator.rin_dicts.items():
        #     book_content = BookofLifeGenerator(
        #         rinpersoon=rinpersoon, recipe_yaml_path=self.recipe,
        #         paragraphs=paragraphs, table_version="").generate_book()
        #     outcome = outcome_dict.get(rinpersoon, "nan")  # Default to "0" if not found