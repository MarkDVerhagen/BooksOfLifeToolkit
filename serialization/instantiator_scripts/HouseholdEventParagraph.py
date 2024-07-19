from dataclasses import dataclass, field
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

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
    HOUSEKEEPING_NR: str = field(default=None)
    # Household type
    TYPHH: str = field(default=None)
    # Household start date
    DATE_STIRTHH: str = field(default=None)
    # Household end date
    DATUMEINDEHH: str = field(default=None)
    # Number of persons in the household
    NUMBERPERSHH: int = field(default=None)
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
    BIRTHEDYOUNGCHILDHH: int = field(default=None)
    # Birth month of the youngest child in the household
    GEBMAANDJONGSTEKINDHH: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # Year of birth of the oldest child in the household
    GEBJAAROUDSTEKINDHH: int = field(default=None)
    # Birth month of the oldest child in the household
    BMAANDOUDSTEKINDHH: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)

    # HOUSEHOLD MEMBER LISTS
    # Children living at home in the household
    CHILDREN: List[str] = field(default_factory=list)
    # Partners living at home in the household
    PARTNERS: List[str] = field(default_factory=list)
    # Other members living at home in the household
    OTHER_MEMBERS: List[str] = field(default_factory=list)
    # All members living at home in the household
    ALL_MEMBERS: List[str] = field(default_factory=list)

    def __post_init__(self):        
        super().__post_init__()
        assert self.dataset_name == 'household_bus', "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'household_bus'"
        
        # set year, month, and day values of parent class from houshold start date
        year, month, day = self.DATE_STIRTHH.split('-')

        # Convert them to integers (if needed)
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        
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
        paragraph = f"On {self.DATE_STIRTHH}, a new household (ID: {self.HOUSEKEEPING_NR}) was formed. "

        household_types = {
            "1": "single-person",
            "2": "unmarried couple without children",
            "3": "married couple without children",
            "4": "unmarried couple with children",
            "5": "married couple with children",
            "6": "single parent",
            "7": "other"
        }

        household_type = household_types.get(self.TYPHH, "unknown type")
        paragraph += f"This was a {household_type} household consisting of {self.NUMBERPERSHH} person{'s' if self.NUMBERPERSHH != 1 else ''}. "

        if self.AANTALKINDHH > 0:
            paragraph += f"The household included {self.AANTALKINDHH} child{'ren' if self.AANTALKINDHH > 1 else ''}. "
            if self.GEBJAAROUDSTEKINDHH and self.GEBJAAROUDSTEKINDHH != self.BIRTHEDYOUNGCHILDHH:
                paragraph += f"The oldest child was born in {self.GEBJAAROUDSTEKINDHH}, while the youngest was born in {self.BIRTHEDYOUNGCHILDHH}. "
            elif self.BIRTHEDYOUNGCHILDHH:
                paragraph += f"The {'only' if self.AANTALKINDHH == 1 else 'youngest'} child was born in {self.BIRTHEDYOUNGCHILDHH}. "

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
        
    
