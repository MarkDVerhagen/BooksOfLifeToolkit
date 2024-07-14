from dataclasses import dataclass, field
from typing import List, Literal
from serial.paragraph import Paragraph

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
    

# household_paragraphs = [
#     HouseholdEventParagraph(
#         dataset_name="household_paragraph_table",  # Table name
#         rinpersoon=12345,                     # Person ID
#         HOUSEKEEPING_NR="12345",             # Unique household identification number
#         TYPHH="Single",                      # Household type
#         DATE_STIRTHH="2020-01-01",           # Household start date
#         DATUMEINDEHH="2021-01-01",           # Household end date
#         NUMBERPERSHH=1,                      # Number of persons in the household
#         PLHH="Head",                         # Place of person in the household
#         REFPERSOONHH="1",                    # Reference person indicator
#         AANTALOVHH=0,                        # Number of other members in the household
#         AANTALKINDHH=0,                      # Number of children living at home in the household
#         BIRTHEDYOUNGCHILDHH=0,               # Year of birth of the youngest child in the household
#         GEBMAANDJONGSTEKINDHH="--",          # Birth month of the youngest child in the household
#         GEBJAAROUDSTEKINDHH=0,               # Year of birth of the oldest child in the household
#         BMAANDOUDSTEKINDHH="--"              # Birth month of the oldest child in the household
#     ),
#     HouseholdEventParagraph(
#         dataset_name="household_paragraph_table",  # Table name
#         rinpersoon=67890,                     # Person ID
#         HOUSEKEEPING_NR="67890",             # Unique household identification number
#         TYPHH="Family",                      # Household type
#         DATE_STIRTHH="2020-01-01",           # Household start date
#         DATUMEINDEHH="2021-01-01",           # Household end date
#         NUMBERPERSHH=4,                      # Number of persons in the household
#         PLHH="Child",                        # Place of person in the household
#         REFPERSOONHH="0",                    # Reference person indicator
#         AANTALOVHH=3,                        # Number of other members in the household
#         AANTALKINDHH=2,                      # Number of children living at home in the household
#         BIRTHEDYOUNGCHILDHH=2010,            # Year of birth of the youngest child in the household
#         GEBMAANDJONGSTEKINDHH="01",          # Birth month of the youngest child in the household
#         GEBJAAROUDSTEKINDHH=2005,            # Year of birth of the oldest child in the household
#         BMAANDOUDSTEKINDHH="12"              # Birth month of the oldest child in the household
#     ),
# ]

# # generate example paragraph string
# for paragraph in household_paragraphs:
#     print(paragraph.get_paragraph_string())