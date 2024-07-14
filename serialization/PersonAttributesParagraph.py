from dataclasses import dataclass, field, fields
from typing import List, Literal
from serial.paragraph import Paragraph

@dataclass
class PersonAttributesParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    """

    ### ORDER OF BELOW IS RELEVANT! ###

    ## BIRTH
    # Country of birth
    GBAGEBOORTELAND: str = field(default=None)
    # Gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHT: Literal["1", "2", "-"] = field(default=None)
    # Year of birth
    GBAGEBOORTEJAAR: int = field(default=None)
    # Month of birth: "01" to "12", "--" - unknown
    GBAGEBOORTEMAAND: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # Day of birth: "01" to "31", "--" - unknown
    GBAGEBOORTEDAG: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    # Country of origin (CBS definition) - the country where the person was born or where parents were born if the person was born in the Netherlands
    GBAHERKOMSTLAND: str = field(default=None)
    # Born in the Netherlands or outside
    # unknown = "-", "0" - born abroad, "1" - born in the Netherlands
    GBAGEBOORTELANDNL: Literal["-", "0", "1"] = field(default=None)
    
    ## MIGRATION BACKGROUND
    # Migration background - CBS definition
    GBAHERKOMSTGROEPERING: str = field(default=None)
    # Migration background - Dutch native, first generation migrant, or second generation migrant
    # "unknown "-"", native (Dutch) "0", first generation migrant "1", second generation migrant "2"
    GBAGENERATIE: Literal["-", "0", "1", "2"] = field(default=None)
    
    ## Parents
    # Number of person's parents born outside of the Netherlands
    # unknown "-", 0 - no parents born abroad, 1 - one parent born abroad, 2 - both parents born abroad
    GBAAANTALOUDERSBUITENLAND: Literal["-", "0", "1", "2"] = field(default=None)
    
    ## MOTHER
    # Country of birth of person's mother
    GBAGEBOORTELANDMOEDER: str = field(default=None)
    # Mother's gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTMOEDER: Literal["1", "2", "-"] = field(default=None)
    # Mother's birth year
    GBAGEBOORTEJAARMOEDER: int = field(default=None)
    # Mother's birth month: "01" to "12", "--" - unknown
    GBAGEBOORTEMAANDMOEDER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # Mother's birth day: "01" to "31", "--" - unknown
    GBAGEBOORTEDAGMOEDER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    
    ## FATHER
    # Country of birth of person's father
    GBAGEBOORTELANDVADER: str = field(default=None)
    # Father's gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTVADER: Literal["1", "2", "-"] = field(default=None)
    # Father's birth year
    GBAGEBOORTEJAARVADER: int = field(default=None)
    # Father's birth month: "01" to "12", "--" - unknown
    GBAGEBOORTEMAANDVADER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # Father's birth day: "01" to "31", "--" - unknown
    GBAGEBOORTEDAGVADER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    
    

    def __post_init__(self):
        assert self.dataset_name == 'persoon_tab', "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = self.GBAGEBOORTEJAAR
        self.month = self.GBAGEBOORTEMAAND
        self.day = self.GBAGEBOORTEDAG


    

# person_paragraphs = [
#     PersonAttributesParagraph(
#         dataset_name="persoon_tab",  # Table name
#         person_id=12345,                     # Person ID
#         GBAGEBOORTELAND="Netherlands",             # Country of birth
#         GBAGESLACHT="1",                       # Gender
#         GBAGEBOORTELANDMOEDER="Germany",                 # Country of birth of person's mother
#         GBAGEBOORTELANDVADER="France",                  # Country of birth of person's father
#         GBAAANTALOUDERSBUITENLAND="1",                       # Number of parents born outside the Netherlands
#         GBAHERKOMSTGROEPERING="group1",                  # Migration background
#         GBAGENERATIE="0",                       # Migration background generation
#         GBAGEBOORTEJAAR=1980,                      # Year of birth
#         GBAGEBOORTEMAAND="01",                      # Month of birth
#         GBAGEBOORTEDAG="01",                      # Day of birth
#         GBAGESLACHTMOEDER="2",                       # Mother's gender
#         GBAGESLACHTVADER="1",                       # Father's gender
#         GBAGEBOORTEJAARMOEDER=1950,                      # Mother's birth year
#         GBAGEBOORTEMAANDMOEDER="02",                      # Mother's birth month
#         GBAGEBOORTEDAGMOEDER="01",                      # Mother's birth day
#         GBAGEBOORTEJAARVADER=1948,                      # Father's birth year
#         GBAGEBOORTEMAANDVADER="03",                      # Father's birth month
#         GBAGEBOORTEDAGVADER="01",                      # Father's birth day
#         GBAHERKOMSTLAND="Netherlands",             # Country of origin
#         GBAGEBOORTELANDNL="1",                       # Born in the Netherlands or outside
#     ),
# ]

# # Convert list of PersonOriginParagraph instances to list of dictionaries
# person_paragraphs_dict_list = [paragraph.__dict__ for paragraph in person_paragraphs]

# # Display the list of dictionaries
# for paragraph in person_paragraphs:
#     print(paragraph.get_paragraph_string_tabular())
