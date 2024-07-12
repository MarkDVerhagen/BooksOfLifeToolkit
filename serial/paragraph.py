"""
The Paragraph class serves as a base class for representing and serializing various types of 
information related to persons in the CBS personal records database.

It includes common attributes that are shared across different paragraph types and provides a framework for 
more specific paragraph classes to build upon.

Attributes:
    year (int): The year the paragraph occurred.
    paragraph_type (str): The category of the paragraph.
    table_name (str): The name of the source database table.
    person_id (int): Unique identifier for the person related to the paragraph.
    paragraph_string (str, init=False): Textual representation of the paragraph (constructed in subclasses).
"""


from dataclasses import dataclass, field
from typing import List, Literal


@dataclass
class Paragraph:
    year: int
    paragraph_type: str 
    is_spell: bool # spell or single paragraph?
    table_name: str
    person_id: int # RINSPERSOON. Is this the main key?
    paragraph_string: str = field(init=False)



@dataclass
class PersonOriginParagraph(Paragraph):

    """
The PersonParagraph class is specifically designed for the GBAPERSOONTAB data table.
It extends the Paragraph class by adding attributes that capture invariant 
personal information such as country of birth, gender, 
parents' birth countries, and more.

Attributes:
    GBAGEBOORTELAND (str): Country of birth.
    GBAGESLACHT (str): Gender (1 - man, 2 - woman, "-" - unknown).
    GBAGEBOORTELANDMOEDER (str): Country of birth of person's mother.
    GBAGEBOORTELANDVADER (str): Country of birth of person's father.
    GBAAANTALOUDERSBUITENLAND (str): Number of person's parents born outside of the Netherlands ("-", "0", "1", "2").
    GBAHERKOMSTGROEPERING (str): Migration background - CBS definition.
    GBAGENERATIE (str): Migration background generation ("-", "0", "1", "2").
    GBAGEBOORTEJAAR (int): Year of birth.
    GBAGESLACHTMOEDER (str): Mother's gender (1 - man, 2 - woman, "-" - unknown).
    GBAGESLACHTVADER (str): Father's gender (1 - man, 2 - woman, "-" - unknown).
    GBAGEBOORTEJAARMOEDER (int): Mother's birth year.
    GBAGEBOORTEJAARVADER (int): Father's birth year.
    GBAHERKOMSTLAND (str): Country of origin.
    GBAGEBOORTELANDNL (str): Born in the Netherlands or outside ("-", "0", "1").
    birthday (str): Person's birthdate.
"""
    # Country of birth
    GBAGEBOORTELAND: str
    
    # Gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHT: Literal["1", "2", "-"]
    
    # Country of birth of person's mother
    GBAGEBOORTELANDMOEDER: str
    
    # Country of birth of person's father
    GBAGEBOORTELANDVADER: str
    
    # Number of person's parents born outside of the Netherlands
    # unknown "-", 0 - no parents born abroad, 1 - one parent born abroad, 2 - both parents born abroad
    GBAAANTALOUDERSBUITENLAND: Literal["-", "0", "1", "2"]
    
    # Migration background - CBS definition
    GBAHERKOMSTGROEPERING: str
    
    # Migration background - Dutch native, first generation migrant, or second generation migrant
    # "unknown "-"", native (Dutch) "0", first generation migrant "1", second generation migrant "2"
    GBAGENERATIE: Literal["-", "0", "1", "2"]
    
    # Year of birth
    GBAGEBOORTEJAAR: int
    
    # Mother's gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTMOEDER: Literal["1", "2", "-"]
    
    # Father's gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTVADER: Literal["1", "2", "-"]
    
    # Mother's birth year
    GBAGEBOORTEJAARMOEDER: int
    
    # Father's birth year
    GBAGEBOORTEJAARVADER: int
    
    # Country of origin (CBS definition) - the country where the person was born or where parents were born if the person was born in the Netherlands
    GBAHERKOMSTLAND: str
    
    # Born in the Netherlands or outside
    # unknown = "-", "0" - born abroad, "1" - born in the Netherlands
    GBAGEBOORTELANDNL: Literal["-", "0", "1"]
    
    # Person's birthdate
    birthday: str

    def __post_init__(self):
        self.year = self.GBAGEBOORTEJAAR

        # The basic serialization is a list of the attributes
        self.paragraph_string = (
            f"person_id: {self.person_id}\n"
            f"GBAGEBOORTELAND: {self.GBAGEBOORTELAND}\n"
            f"GBAGESLACHT: {self.GBAGESLACHT}\n"
            f"GBAGEBOORTELANDMOEDER: {self.GBAGEBOORTELANDMOEDER}\n"
            f"GBAGEBOORTELANDVADER: {self.GBAGEBOORTELANDVADER}\n"
            f"GBAAANTALOUDERSBUITENLAND: {self.GBAAANTALOUDERSBUITENLAND}\n"
            f"GBAHERKOMSTGROEPERING: {self.GBAHERKOMSTGROEPERING}\n"
            f"GBAGENERATIE: {self.GBAGENERATIE}\n"
            f"GBAGEBOORTEJAAR: {self.GBAGEBOORTEJAAR}\n"
            f"GBAGESLACHTMOEDER: {self.GBAGESLACHTMOEDER}\n"
            f"GBAGESLACHTVADER: {self.GBAGESLACHTVADER}\n"
            f"GBAGEBOORTEJAARMOEDER: {self.GBAGEBOORTEJAARMOEDER}\n"
            f"GBAGEBOORTEJAARVADER: {self.GBAGEBOORTEJAARVADER}\n"
            f"GBAHERKOMSTLAND: {self.GBAHERKOMSTLAND}\n"
            f"GBAGEBOORTELANDNL: {self.GBAGEBOORTELANDNL}\n"
            f"birthday: {self.birthday}"
        )
        self.paragraph_type = "person_paragraph"
        self.table_name = "person_paragraph_table"

    def simple_string(self):
        data_string = None
        return data_string

# Create instances of PersonParagraph
person_paragraphs = [
    PersonOriginParagraph(1980, "person_paragraph", "person_paragraph_table", 12345, "Netherlands", "1", "Germany", "France", "1", "group1", "0", 1980, "2", "1", 1950, 1948, "Netherlands", "1", "1980-01-01"),
    PersonOriginParagraph(1990, "person_paragraph", "person_paragraph_table", 67890, "USA", "2", "Canada", "Mexico", "2", "group2", "1", 1990, "1", "2", 1960, 1958, "USA", "0", "1990-05-15"),
    PersonOriginParagraph(1975, "person_paragraph", "person_paragraph_table", 13579, "Japan", "-", "China", "South Korea", "-", "group3", "2", 1975, "-", "2", 1945, 1943, "Japan", "-", "1975-07-30")
]

# Convert list of PersonOriginParagraph instances to list of dictionaries
person_paragraphs_dict_list = [paragraph.__dict__ for paragraph in person_paragraphs]

# Display the list of dictionaries
for paragraph in person_paragraphs:
    print(paragraph.paragraph_string)
