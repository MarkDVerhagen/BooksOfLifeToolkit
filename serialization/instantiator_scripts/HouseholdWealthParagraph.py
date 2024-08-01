from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph


@dataclass
class HouseholdWealthParagraph(Paragraph):
    """
    The HouseholdWealthParagraph class is specifically designed for the VEHTAB data table (2006-2022).
    It extends the Paragraph class by adding attributes that capture household wealth/assets info
    from January 1 of the reporting year of the household.
    name: wealth_tab
    """

    ### ORDER OF BELOW IS RELEVANT! ###

    ## Together, codes identify main breadwinner of household
    RINPERSOONSHKW: Literal["F", "R", "S"] = field(default=None)
    RINPERSOONHKW: str = field(default=None)
    
    ## Note: percentiles go from 1-100, with -1 = private household w/unknown income and 
    ## -2 = institutional household

    ## for assets variables: 99999999999 = household w/no perceived income

    # General wealth

    ## Percentile group of household prosperity (based on assets and standardized income)
    VEHP100WELVAART: int = field(default=None)
    ## Percentile group of private household wealth (assets)
    VEHP100HVERM: int = field(default=None)
    ## Value of a household's total assets 
    VEHW1000VERH: float = field(default=None)
     ## Value of household total debt
    VEHW1200STOH: float = field(default=None)

    # Specific assets 

    ## Value of household posessions (bank and savings deposits and securities, bonds and shares, 
    ## owner-occupied home, business assets, and other assets)
    VEHW1100BEZH: float = field(default=None)
    ## Value of household financial assets (bank and savings deposits and securities)
    VEHW1110FINH: float = field(default=None)
    ## Value of household bank and savings balances (household's deposits on accounts at banks)
    VEHW1111BANH: float = field(default=None)
    ## Value of household bonds and shares
    VEHW1112EFFH: float = field(default=None)
    ## Value of household real estate
    VEHW1120ONRH: float = field(default=None)
    ## Value of principal residence home owned by houshold 
    VEHW1121WONH: float = field(default=None)
    ## Value of other household real estate (excluding principal residence)
    VEHW1122OGOH: float = field(default=None)
    ## Value of household assets excluding owner-occupied home and mortgage debt
    VEHWVEREXEWH: float = field(default=None)
    ## Value of household's business/professional assets
    VEHW1130ONDH: float = field(default=None)
    ## Value of significant interest of a household (share of at least 5% in issued share capital of a company)
    VEHW1140ABEH: float = field(default=None)
    ## Value of household's other assets
    VEHW1150OVEH: float = field(default=None)

    # Specific debts
    ## Value of household's mortgage debt
    VEHW1210SHYH: float = field(default=None)
    ## Value of household's student debt
    VEHW1220SSTH: float = field(default=None)
    ## Value of household's other debts
    VEHW1230SOVH: float = field(default=None)
    

    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name == 'wealth_tab', "This class is specifically designed for the VEHTAB data table. Dataset name must be 'wealth_tab'"

        ## TODO: year, month, day 
        ## TODO: clean assets variables to exclude negative percentile, no perceived income field


    def get_paragraph_string_biographic(self, features=None):
        pass
