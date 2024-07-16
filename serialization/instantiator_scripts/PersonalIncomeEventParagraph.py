from dataclasses import dataclass, field
from typing import List, Literal
from instantiator_scripts.Paragraph import Paragraph

@dataclass
class PersonalIncomeEventParagraph(Paragraph):
    """
    The PersonalIncomeEventParagraph class is specifically designed for the inpatab data table.
    It extends the Paragraph class by adding attributes that capture relevant information
    for a person's decision to start a family and have children.
    name: inpa_tab
    """

    ### ORDER OF BELOW IS RELEVANT! ###

    ## INCOME
    # Personal gross income
    INPPERSBRUT: float = field(default=None)
    # Personal primary income
    INPPERSPRIM: float = field(default=None)
    # Economic independence indicator
    INPEMEZE: Literal["0", "1", "8", "9"] = field(default=None)
    # Financial independence indicator
    INPEMFO: Literal["0", "1", "8", "9"] = field(default=None)
    # Income from own business
    INPT2070WIN: float = field(default=None)
    # Pensions and annuities
    INPT5280PEN: float = field(default=None)
    
    ## EMPLOYMENT
    # Socioeconomic category on an annual basis
    INPSECJ: str = field(default=None)
    # Type of self-employed
    INPTYPZLF: Literal["0", "1", "2", "3", "4", "9"] = field(default=None)
    
    ## EDUCATION
    # Study financing
    INPT6330STU: float = field(default=None)
    
    ## SOCIAL BENEFITS
    # Child benefit
    INPT6320KB: float = field(default=None)
    # Child-related budget
    INPT6325KGB: float = field(default=None)
    # Rent allowance
    INPT7340HRS: float = field(default=None)
    # Unemployment benefits
    INPT5210WW: float = field(default=None)
    # Disability benefits
    INPT5240AO: float = field(default=None)
    # Old-age pension
    INPT5260AOW: float = field(default=None)
    
    ## ASSETS AND DEBTS
    # Income from own home
    INPT3160OVB: float = field(default=None)
    # Mortgage interest paid
    INPT3170RBW: float = field(default=None)
    # Interest paid on other debts
    INPT3180RST: float = field(default=None)
    
    ## PURCHASING POWER
    # Purchasing power mutation
    INPKMUTH: float = field(default=None)
    
    ## TAX-RELATED
    # Income tax owed
    INPV3900INK: float = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name == 'inpatab', "This class is specifically designed for the inpatab data table. Dataset name must be 'inpatab'"

    def get_paragraph_string_family_decision(self):
        paragraph = ""

        # Income
        if self.INPPERSBRUT is not None:
            paragraph += f"Their gross personal income is €{self.INPPERSBRUT:.2f}. "
        if self.INPPERSPRIM is not None:
            paragraph += f"Their primary personal income is €{self.INPPERSPRIM:.2f}. "
        if self.INPT2070WIN is not None and self.INPT2070WIN > 0:
            paragraph += f"They have an income of €{self.INPT2070WIN:.2f} from their own business. "
        if self.INPT5280PEN is not None and self.INPT5280PEN > 0:
            paragraph += f"They receive €{self.INPT5280PEN:.2f} in pensions and annuities. "

        # Economic and Financial Independence
        if self.INPEMEZE == "1":
            paragraph += "They are considered economically independent. "
        if self.INPEMFO == "1":
            paragraph += "They are considered financially independent. "

        # Employment
        employment_categories = {
            "11": "Employee", "12": "Director-major shareholder", "13": "Self-employed", "14": "Other self-employed",
            "21": "Receiving unemployment benefits", "22": "Receiving welfare benefits", "23": "Receiving other social benefits",
            "31": "Receiving pension"
        }
        if self.INPSECJ in employment_categories:
            paragraph += f"Their employment status is categorized as '{employment_categories[self.INPSECJ]}'. "

        self_employed_types = {
            "1": "Self-employed with staff", "2": "Self-employed without staff, own work",
            "3": "Self-employed without staff, products", "4": "Other self-employed"
        }
        if self.INPTYPZLF in self_employed_types:
            paragraph += f"They are classified as '{self_employed_types[self.INPTYPZLF]}'. "

        # Education
        if self.INPT6330STU is not None and self.INPT6330STU > 0:
            paragraph += f"They are receiving €{self.INPT6330STU:.2f} in study financing, which suggests they might be a student. "

        # Social benefits
        if self.INPT6320KB is not None and self.INPT6320KB > 0:
            paragraph += f"They are receiving €{self.INPT6320KB:.2f} in child benefits. "
        if self.INPT6325KGB is not None and self.INPT6325KGB > 0:
            paragraph += f"They are receiving €{self.INPT6325KGB:.2f} as a child-related budget. "
        if self.INPT7340HRS is not None and self.INPT7340HRS > 0:
            paragraph += f"They are receiving €{self.INPT7340HRS:.2f} in rent allowance. "
        if self.INPT5210WW is not None and self.INPT5210WW > 0:
            paragraph += f"They are receiving €{self.INPT5210WW:.2f} in unemployment benefits. "
        if self.INPT5240AO is not None and self.INPT5240AO > 0:
            paragraph += f"They are receiving €{self.INPT5240AO:.2f} in disability benefits. "
        if self.INPT5260AOW is not None and self.INPT5260AOW > 0:
            paragraph += f"They are receiving €{self.INPT5260AOW:.2f} in old-age pension. "

        # Assets and debts
        if self.INPT3160OVB is not None:
            paragraph += f"Their income from own home is €{self.INPT3160OVB:.2f}. "
        if self.INPT3170RBW is not None and self.INPT3170RBW > 0:
            paragraph += f"They paid €{self.INPT3170RBW:.2f} in mortgage interest. "
        if self.INPT3180RST is not None and self.INPT3180RST > 0:
            paragraph += f"They paid €{self.INPT3180RST:.2f} in interest on other debts. "

        # Purchasing power
        if self.INPKMUTH is not None:
            paragraph += f"Their purchasing power mutation is {self.INPKMUTH/100000:.2f}%. "

        # Tax
        if self.INPV3900INK is not None:
            paragraph += f"They owe €{self.INPV3900INK:.2f} in income tax. "

        paragraph += "These factors may influence their decision to start or expand their family."

        return paragraph.strip()