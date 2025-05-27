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
class LisaAttributesParagraph(Paragraph):
    """
    The PersonOriginParagraph class is specifically designed for the GBAPERSOONTAB data table.
    It extends the Paragraph class by adding attributes that capture invariant personal information 
    such as country of birth, gender, parents' birth countries, and more.
    name: persoon_tab
    """
    VZAFSTANDKDV: str = field(default=None)
    VZAANTKDV01KM: str = field(default=None)
    VZAANTKDV03KM: str = field(default=None)
    VZAANTKDV05KM: str = field(default=None)
    VZAFSTANDBSO: str = field(default=None)
    VZAANTBSO01KM: str = field(default=None)
    VZAANTBSO03KM: str = field(default=None)
    VZAANTBSO05KM: str = field(default=None)
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
    VEHP100HVERM: str = field(default=None)
    INPBELI : str = field(default=None)
    INPEMEZ: str = field(default=None)
    INPEMFO: str = field(default=None)
    INPP100PBRUT: str = field(default=None)
    INPP100PPERS: str = field(default=None)
    INPPERSPRIM: str = field(default=None)
    INPPINK: str = field(default=None)
    INPPOSHHK: str = field(default=None)
    INHAHL: str = field(default=None)
    INHAHLMI: str = field(default=None)
    INHARMEUR: str = field(default=None)
    INHARMEURL: str = field(default=None)
    INHBBIHJ: str = field(default=None)
    INHBRUTINKH: str = field(default=None)
    VEHW1000VERH : str = field(default=None)
    birthday_youngest: str = field(default=None)
    marriages_total : str = field(default=None)
    partnerships_total: str = field(default=None)
    GBABURGERLIJKESTAATNW: str = field(default=None)
    AANVANGVERBINTENIS: str = field(default=None)
    GBAGEBOORTEJAARPARTNER: str = field(default=None)
    GBAGEBOORTEMAANDPARTNER: str = field(default=None)
    GBAGEBOORTELANDPARTNER: str = field(default=None)
    GBAGESLACHTPARTNER: str = field(default=None)
    OPLNIVSOI2021AGG4HBmetNIRWO_partner: str = field(default=None)
    OPLNIVSOI2021AGG4HGmetNIRWO_partner: str = field(default=None)
    SECM_partner: str = field(default=None)
    children_pre2021: str = field(default=None)

    def __post_init__(self):
        # super().__post_init__()
        assert self.dataset_name.startswith('lisa_tab'), "This class is specifically designed for the GBAPERSOONTAB data table. Dataset name must be 'persoon_tab'"

        self.year = int(2020)
        self.month = "12"
        self.day = "31"
        self.year_dataset_name = self.dataset_name + '_' + str(self.year)
        self.year_month_day = '_'.join([str(self.year), str(self.month), str(self.day)])
        self.VZAFSTANDKDV = self.VZAFSTANDKDV.replace(".0", "") if self.VZAFSTANDKDV else 'nan' 
        self.VZAANTKDV01KM = self.VZAANTKDV01KM.replace(".0", "") if self.VZAANTKDV01KM else 'nan' 
        self.VZAANTKDV03KM = self.VZAANTKDV03KM.replace(".0", "") if self.VZAANTKDV03KM else 'nan' 
        self.VZAANTKDV05KM = self.VZAANTKDV05KM.replace(".0", "") if self.VZAANTKDV05KM else 'nan' 
        self.VZAFSTANDBSO = self.VZAFSTANDBSO.replace(".0", "") if self.VZAFSTANDBSO else 'nan' 
        self.VZAANTBSO01KM = self.VZAANTBSO01KM.replace(".0", "") if self.VZAANTBSO01KM else 'nan' 
        self.VZAANTBSO03KM = self.VZAANTBSO03KM.replace(".0", "") if self.VZAANTBSO03KM else 'nan' 
        self.VZAANTBSO05KM = self.VZAANTBSO05KM.replace(".0", "") if self.VZAANTBSO05KM else 'nan' 
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
        self.VEHP100HVERM = self.VEHP100HVERM.replace(".0", "") if self.VEHP100HVERM else 'nan' 
        self.INPBELI  = self.INPBELI.replace(".0", "") if self.INPBELI  else 'nan' 
        self.INPEMEZ = self.INPEMEZ.replace(".0", "") if self.INPEMEZ else 'nan' 
        self.INPEMFO = self.INPEMFO.replace(".0", "") if self.INPEMFO else 'nan' 
        self.INPP100PBRUT = self.INPP100PBRUT.replace(".0", "") if self.INPP100PBRUT else 'nan' 
        self.INPP100PPERS = self.INPP100PPERS.replace(".0", "") if self.INPP100PPERS else 'nan' 
        self.INPPERSPRIM = self.INPPERSPRIM.replace(".0", "") if self.INPPERSPRIM else 'nan' 
        self.INPPINK = self.INPPINK.replace(".0", "") if self.INPPINK else 'nan' 
        self.INPPOSHHK = self.INPPOSHHK.replace(".0", "") if self.INPPOSHHK else 'nan' 
        self.INHAHL = self.INHAHL.replace(".0", "") if self.INHAHL else 'nan' 
        self.INHAHLMI = self.INHAHLMI.replace(".0", "") if self.INHAHLMI else 'nan' 
        self.INHARMEUR = self.INHARMEUR.replace(".0", "") if self.INHARMEUR else 'nan' 
        self.INHARMEURL = self.INHARMEURL.replace(".0", "") if self.INHARMEURL else 'nan' 
        self.INHBBIHJ = self.INHBBIHJ.replace(".0", "") if self.INHBBIHJ else 'nan' 
        self.INHBRUTINKH = self.INHBRUTINKH.replace(".0", "") if self.INHBRUTINKH else 'nan' 
        self.VEHW1000VERH  = self.VEHW1000VERH .replace(".0", "") if self.VEHW1000VERH  else 'nan' 
        self.children_pre2021 = self.children_pre2021.replace(".0", "")
        self.birthday_youngest = make_date(self.birthday_youngest[6:8], self.birthday_youngest[4:6], self.birthday_youngest[:4])
        self.marriages_total = self.marriages_total .replace(".0", "")
        self.partnerships_total = self.partnerships_total.replace(".0", "")
        self.GBABURGERLIJKESTAATNW = self.GBABURGERLIJKESTAATNW.replace(".0", "") if self.GBABURGERLIJKESTAATNW else 'nan' 
        self.AANVANGVERBINTENIS = make_date(self.AANVANGVERBINTENIS[6:8], self.AANVANGVERBINTENIS[4:6], self.AANVANGVERBINTENIS[:4])
        self.GBAGEBOORTEJAARPARTNER = self.GBAGEBOORTEJAARPARTNER.replace(".0", "") if self.GBAGEBOORTEJAARPARTNER else 'nan' 
        self.GBAGEBOORTEMAANDPARTNER = self.GBAGEBOORTEMAANDPARTNER.replace(".0", "") if self.GBAGEBOORTEMAANDPARTNER else 'nan' 
        self.GBAGEBOORTELANDPARTNER = self.GBAGEBOORTELANDPARTNER.replace(".0", "") if self.GBAGEBOORTELANDPARTNER else 'nan' 
        self.GBAGESLACHTPARTNER = self.GBAGESLACHTPARTNER.replace(".0", "") if self.GBAGESLACHTPARTNER else 'nan' 
        self.OPLNIVSOI2021AGG4HBmetNIRWO_partner = self.OPLNIVSOI2021AGG4HBmetNIRWO_partner.replace(".0", "") if self.OPLNIVSOI2021AGG4HBmetNIRWO_partner else 'nan' 
        self.OPLNIVSOI2021AGG4HGmetNIRWO_partner = self.OPLNIVSOI2021AGG4HGmetNIRWO_partner.replace(".0", "") if self.OPLNIVSOI2021AGG4HGmetNIRWO_partner else 'nan' 
        self.SECM_partner = self.SECM_partner.replace(".0", "") if self.SECM_partner else 'nan' 