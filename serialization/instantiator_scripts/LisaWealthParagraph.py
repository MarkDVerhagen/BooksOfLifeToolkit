from dataclasses import dataclass, field, fields
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
class LisaWealthParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
    """
    INHEHALGR : str = field(default=None)
    INHPOPIIV: str = field(default=None)
    INHSAMAOW: str = field(default=None)
    INHSAMHH: str = field(default=None)
    INHUAF: str = field(default=None)
    INHUAFL: str = field(default=None)
    INHUAFTYP: str = field(default=None)
    VEHW1100BEZH: str = field(default=None)
    VEHW1110FINH: str = field(default=None)
    VEHW1120ONRH: str = field(default=None)
    VEHW1130ONDH: str = field(default=None)
    VEHW1140ABEH: str = field(default=None)
    VEHW1150OVEH: str = field(default=None)
    VEHW1200STOH: str = field(default=None)
    VEHW1210SHYH: str = field(default=None)
    VEHW1220SSTH: str = field(default=None)
    VEHW1230SOVH: str = field(default=None)
    VEHWVEREXEWH: str = field(default=None)
    VEHP100WELVAART: str = field(default=None)
    VEHW1000VERH: str = field(default=None)
    VEHP100HVERM: str = field(default=None)
    
    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('wealth_lisa_tab'), "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = int(2020)
        self.month = "12"
        self.day = "31"
        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), str(self.month), str(self.day)])
        self.INHEHALGR  = self.INHEHALGR.replace(".0", "") if self.INHEHALGR  else 'nan' 
        self.INHPOPIIV = self.INHPOPIIV.replace(".0", "") if self.INHPOPIIV else 'nan' 
        self.INHSAMAOW = self.INHSAMAOW.replace(".0", "") if self.INHSAMAOW else 'nan' 
        self.INHSAMHH = self.INHSAMHH.replace(".0", "") if self.INHSAMHH else 'nan' 
        self.INHUAF = self.INHUAF.replace(".0", "") if self.INHUAF else 'nan' 
        self.INHUAFL = self.INHUAFL.replace(".0", "") if self.INHUAFL else 'nan' 
        self.INHUAFTYP = self.INHUAFTYP.replace(".0", "") if self.INHUAFTYP else 'nan' 
        self.VEHW1100BEZH = self.VEHW1100BEZH.replace(".0", "") if self.VEHW1100BEZH else 'nan' 
        self.VEHW1110FINH = self.VEHW1110FINH.replace(".0", "") if self.VEHW1110FINH else 'nan' 
        self.VEHW1120ONRH = self.VEHW1120ONRH.replace(".0", "") if self.VEHW1120ONRH else 'nan' 
        self.VEHW1130ONDH = self.VEHW1130ONDH.replace(".0", "") if self.VEHW1130ONDH else 'nan' 
        self.VEHW1140ABEH = self.VEHW1140ABEH.replace(".0", "") if self.VEHW1140ABEH else 'nan' 
        self.VEHW1150OVEH = self.VEHW1150OVEH.replace(".0", "") if self.VEHW1150OVEH else 'nan' 
        self.VEHW1200STOH = self.VEHW1200STOH.replace(".0", "") if self.VEHW1200STOH else 'nan' 
        self.VEHW1210SHYH = self.VEHW1210SHYH.replace(".0", "") if self.VEHW1210SHYH else 'nan' 
        self.VEHW1220SSTH = self.VEHW1220SSTH.replace(".0", "") if self.VEHW1220SSTH else 'nan' 
        self.VEHW1230SOVH = self.VEHW1230SOVH.replace(".0", "") if self.VEHW1230SOVH else 'nan' 
        self.VEHWVEREXEWH = self.VEHWVEREXEWH.replace(".0", "") if self.VEHWVEREXEWH else 'nan' 
        self.VEHP100WELVAART = self.VEHP100WELVAART.replace(".0", "") if self.VEHP100WELVAART else 'nan' 
        self.VEHW1000VERH = self.VEHW1000VERH.replace(".0", "") if self.VEHW1000VERH else 'nan' 
        self.VEHP100HVERM = self.VEHP100HVERM.replace(".0", "") if self.VEHP100HVERM else 'nan' 