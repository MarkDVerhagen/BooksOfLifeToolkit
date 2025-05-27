from dataclasses import dataclass, field
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

def make_date(day, month, year):
    month_names = {
                "01": "Jan",
                "02": "Feb",
                "03": "Mar",
                "04": "Apr",
                "05": "May",
                "06": "Jun",
                "07": "Jul",
                "08": "Aug",
                "09": "Sep",
                "10": "Oct",
                "11": "Nov",
                "12": "Dec"
            }
    month_acronym = month_names.get(month, "unknown month")
    return ' '.join([month_acronym, day, year])


@dataclass
class HouseholdEventParagraph(Paragraph):
    """The HouseholdCharacteristics class is designed for the dataset that includes household
    characteristics of persons registered in the Municipal Personal Data Administration (GBA).
    It includes attributes such as household start and end dates, household type, number of persons 
    in the household, and more.
    name: household_bus
    """
    ## HOUSEHOLD
    # Unique household identification number
    HUISHOUDNR: str = field(default=None)
    # Household type
    TYPHH: str = field(default=None)
    # Household start date
    DATUMAANVANGHH: str = field(default=None)
    # Household end date
    DATUMEINDEHH: str = field(default=None)
    # Number of persons in the household
    AANTALPERSHH: int = field(default=None)
    # Place of person in the household
    PLHH: str = field(default=None)
    # Reference person indicator (0: no, 1: yes)
    REFPERSOONHH: Literal["0", "1"] = field(default=None)
    # Number of other members in the household
    AANTALOVHH: int = field(default=None)

    ## CHILDREN
    # Number of children living at home in the household
    AANTALKINDHH: int = field(default=None)
    # Year of birth of the youngest child in the household
    GEBJAARJONGSTEKINDHH: int = field(default=None)
    # Birth month of the youngest child in the household
    GEBMAANDJONGSTEKINDHH: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # Year of birth of the oldest child in the household
    GEBJAAROUDSTEKINDHH: int = field(default=None)
    # Birth month of the oldest child in the household
    GEBMAANDOUDSTEKINDHH: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)

    # HOUSEHOLD MEMBER LISTS
    # Children living at home in the household
    CHILDREN: List[str] = field(default_factory=list)
    # Partners living at home in the household
    PARTNERS: List[str] = field(default_factory=list)
    # Other members living at home in the household
    OTHER_MEMBERS: List[str] = field(default_factory=list)
    # All members living at home in the household
    # ALL_MEMBERS: List[str] = field(default_factory=list)


    def __post_init__(self):        
        # super().__post_init__()
        assert self.dataset_name.startswith('household_bus'), "This class is specifically designed for the GBAHUISHOUDENSBUS data table. Dataset name must be 'household_bus'"
        
        # set year, month, and day values of parent class from houshold start date
        year = self.DATUMAANVANGHH[:4]
        month = self.DATUMAANVANGHH[4:6]
        day = self.DATUMAANVANGHH[6:8]

        # Convert them to integers (if needed)
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        
        # Spell start and end
        self.spell_year_end = int(self.DATUMEINDEHH[:4])
        self.spell_year_start = int(self.DATUMAANVANGHH[:4])
        
        # Formatted date
        self.DATUMAANVANGHH = make_date(self.DATUMAANVANGHH[6:8],
                                        self.DATUMAANVANGHH[4:6], self.DATUMAANVANGHH[:4])
        self.DATUMEINDEHH = make_date(self.DATUMEINDEHH[6:8],
                                        self.DATUMEINDEHH[4:6], self.DATUMEINDEHH[:4]) if self.DATUMEINDEHH[:4] != "2050" else "Ongoing"

        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([year, month, day])
        return

    def instantiate_social_context_paragraphs(self, social_context_features):
        result = {}
        for dataset in social_context_features:
            dataset_name = list(dataset.keys())[0]
            result[dataset_name] = {}
            for context, features in dataset[dataset_name].items():
                result[dataset_name][context] = BookofLifeGenerator("03c6605f", {
                    'main_key': self.recipe.main_key,
                    'datasets': features,
                    'formatting': {
                        'sorting_keys': self.recipe.sorting_keys,
                        'paragraph_generator': 'get_paragraph_string_tabular'
                    }
                })
        return result

    def get_paragraph_string_biographic(self, features=None):
            
        household_types = {
                "1": "single-person",
                "2": "unmarried couple without children",
                "3": "married couple without children",
                "4": "unmarried couple with children",
                "5": "married couple with children",
                "6": "single parent",
                "7": "other"
            }
        
        household_place = {
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
        paragraph = f"On {self.DATUMAANVANGHH}, a new household (ID: {self.HUISHOUDNR}) was formed. "

        household_type = household_types.get(self.TYPHH, "unknown type")
        paragraph += f"This was a {household_type} household consisting of {self.AANTALPERSHH} person{'s' if self.AANTALPERSHH != 1 else ''}. "

        if self.AANTALKINDHH > 0:
            paragraph += f"The household included {self.AANTALKINDHH} child{'ren' if self.AANTALKINDHH > 1 else ''}. "
            if self.GEBJAAROUDSTEKINDHH and self.GEBJAAROUDSTEKINDHH != self.GEBJAARJONGSTEKINDHH:
                paragraph += f"The oldest child was born in {self.GEBJAAROUDSTEKINDHH}, while the youngest was born in {self.GEBJAARJONGSTEKINDHH}. "
            elif self.GEBJAARJONGSTEKINDHH:
                paragraph += f"The {'only' if self.AANTALKINDHH == 1 else 'youngest'} child was born in {self.GEBJAARJONGSTEKINDHH}. "

        if self.AANTALOVHH > 0:
            paragraph += f"Besides the reference person and any children, there {'was' if self.AANTALOVHH == 1 else 'were'} {self.AANTALOVHH} other household member{'s' if self.AANTALOVHH > 1 else ''}. "

        if self.DATUMEINDEHH:
            paragraph += f"This household configuration lasted until {self.DATUMEINDEHH}. "
        else:
            paragraph += "This household configuration is still current as of the latest record. "

        if self.CHILDREN is not None and self.PARTNERS is not None and self.OTHER_MEMBERS is not None:
            paragraph += f"The person lives with their partner{'s' if len(self.PARTNERS) > 1 else ''} ({', '.join(str(p) for p in self.PARTNERS)}), child{'ren' if len(self.CHILDREN) > 1 else ''} ({', '.join(str(c) for c in self.CHILDREN)}), and other household member{'s' if len(self.OTHER_MEMBERS) > 1 else ''} ({', '.join(str(o) for o in self.OTHER_MEMBERS)})."
        elif self.CHILDREN is not None and self.PARTNERS is not None:
            paragraph += f"The person lives with their partner{'s' if len(self.PARTNERS) > 1 else ''} ({', '.join(str(p) for p in self.PARTNERS)}) and child{'ren' if len(self.CHILDREN) > 1 else ''} ({', '.join(str(c) for c in self.CHILDREN)})."

        return paragraph.strip()
        
    
