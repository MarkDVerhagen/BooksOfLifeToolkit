from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph


@dataclass
class PersonAttributesParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
        
    Average token length of default book: 89
    Std. Dev. token length of default book: -
    """

    ### ORDER OF BELOW IS RELEVANT! ###

    ## BIRTH
    # Country of birth
    GBAGEBOORTELAND: str = field(default=None)
    # Gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHT: Literal["1", "2", "-"] = field(default=None)
    # Year of birth
    GBAGEBOORTEJAAR: str = field(default=None)
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
    GBAGEBOORTEJAARMOEDER: str = field(default=None)
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
    GBAGEBOORTEJAARVADER: str = field(default=None)
    # Father's birth month: "01" to "12", "--" - unknown
    GBAGEBOORTEMAANDVADER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # Father's birth day: "01" to "31", "--" - unknown
    GBAGEBOORTEDAGVADER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    
    

    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name.startswith('persoon_tab'), "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = int(self.GBAGEBOORTEJAAR)
        self.month = self.GBAGEBOORTEMAAND
        self.day = self.GBAGEBOORTEDAG

    def get_paragraph_string_biographic(self, features=None):
        paragraph = ""

        # Gender
        gender_map = {"1": "male", "2": "female", "-": "unknown gender"}
        gender = gender_map.get(self.GBAGESLACHT, "unknown gender")

        # Birth information
        birth_date = f"{self.GBAGEBOORTEJAAR}"
        if self.GBAGEBOORTEMAAND != "--":
            birth_date += f"-{self.GBAGEBOORTEMAAND}"
            if self.GBAGEBOORTEDAG != "--":
                birth_date += f"-{self.GBAGEBOORTEDAG}"
        
        paragraph += f"This individual is a {gender} person born on {birth_date} in {self.GBAGEBOORTELAND}. "

        # Migration background
        if self.GBAGENERATIE == "0":
            paragraph += "They are a native Dutch person. "
        elif self.GBAGENERATIE == "1":
            paragraph += "They are a first-generation migrant. "
        elif self.GBAGENERATIE == "2":
            paragraph += "They are a second-generation migrant. "

        if self.GBAHERKOMSTGROEPERING:
            paragraph += f"Their migration background is classified as {self.GBAHERKOMSTGROEPERING}. "

        # Parents' information
        if self.GBAAANTALOUDERSBUITENLAND == "0":
            paragraph += "Both of their parents were born in the Netherlands. "
        elif self.GBAAANTALOUDERSBUITENLAND == "1":
            paragraph += "One of their parents was born outside the Netherlands. "
        elif self.GBAAANTALOUDERSBUITENLAND == "2":
            paragraph += "Both of their parents were born outside the Netherlands. "

        # Mother's information
        if self.GBAGEBOORTELANDMOEDER:
            mother_birth_date = f"{self.GBAGEBOORTEJAARMOEDER or 'unknown year'}"
            if self.GBAGEBOORTEMAANDMOEDER != "--":
                mother_birth_date += f"-{self.GBAGEBOORTEMAANDMOEDER}"
                if self.GBAGEBOORTEDAGMOEDER != "--":
                    mother_birth_date += f"-{self.GBAGEBOORTEDAGMOEDER}"
            paragraph += f"Their mother was born on {mother_birth_date} in {self.GBAGEBOORTELANDMOEDER}. "

        # Father's information
        if self.GBAGEBOORTELANDVADER:
            father_birth_date = f"{self.GBAGEBOORTEJAARVADER or 'unknown year'}"
            if self.GBAGEBOORTEMAANDVADER != "--":
                father_birth_date += f"-{self.GBAGEBOORTEMAANDVADER}"
                if self.GBAGEBOORTEDAGVADER != "--":
                    father_birth_date += f"-{self.GBAGEBOORTEDAGVADER}"
            paragraph += f"Their father was born on {father_birth_date} in {self.GBAGEBOORTELANDVADER}. "

        return paragraph.strip()


    

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
