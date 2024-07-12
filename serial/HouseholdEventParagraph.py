from dataclasses import dataclass, field
from typing import List, Literal
from Paragraph import Paragraph

@dataclass
class HouseholdEventParagraph(Paragraph):
    """The HouseholdCharacteristics class is designed for the dataset that includes household
    characteristics of persons registered in the Municipal Personal Data Administration (GBA).
    It includes attributes such as household start and end dates, household type, number of persons 
    in the household, and more.
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
    
    def get_paragraph_string(self, excluded_features_list=None):
        return super().get_paragraph_string(excluded_features_list)