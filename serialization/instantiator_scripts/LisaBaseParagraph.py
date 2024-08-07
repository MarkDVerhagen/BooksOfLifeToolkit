from dataclasses import dataclass, field, fields
from typing import List, Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

@dataclass
class LisaBaseParagraph(Paragraph):
    """
    The LisaBaseParagraph class is specifically designed for Lisa's base dataset.
    It extends the Paragraph class by adding attributes that capture demographic and
    household info, contextual info about previous fertility, housing, employment,
    income, and wealth, as well as other constructed variables related to fertility.
    name: lisa_tab
    """

    ### Order exactly follows order of the Lisa dataset ###

    ## Existing children

    # number of children (biological, adopted) born before 2021
    children_pre2021: int = field(default=None)
    # birthday of the youngest child (biological or adopted) a person has
    birthday_youngest: str = field(default=None) ## unclear what format this is in
    birthyear_youngest: int = field(default=None) # TL added this
    birthmonth_youngest: Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)
    
    ## Personal time-invariant info

    # Country of birth
    # TODO: TL pulled country codes from here (https://www.ssb.no/en/klass/klassifikasjoner/91) but unsure if that's right
    GBAGEBOORTELAND: Literal["000", "101", "102", "103", "104", "105", "106", "111", "112",
                             "113", "114", "115", "117", "118", "119", "120", "121", "122", 
                             "123", "124", "126", "127", "128", "129", "130", "131", "132",
                             "133", "134", "136", "137", "138", "139", "140", "141", "143",
                             "144", "146", "148", "152", "153", "154", "155", "156", "157",
                             "158", "159", "160", "161", "162", "163", "164", "203", "204",
                             "205", "209", "213", "216", "220", "229", "235", "239", "241",
                             "246", "249", "250", "254", "256", "260", "264", "266", "270",
                             "273", "276", "278", "279", "281", "283", "286", "289", "296",
                             "299", "303", "304", "306", "307", "308", "309", "313", "319",
                             "322", "323", "326", "329", "333", "336", "337", "338", "339",
                             "346", "355", "356", "357", "359", "369", "373", "376", "386",
                             "389", "393", "404", "406", "407", "409", "410", "412", "416",
                             "420", "424", "426", "428", "430", "432", "436", "444", "448", 
                             "452", "456", "460", "464", "476", "478", "480", "484", "488",
                             "492", "496", "500", "502", "504", "508", "510", "512", "513",
                             "516", "520", "524", "528", "534", "537", "540", "544", "548",
                             "550", "552", "554", "564", "568", "575", "578", "601", "602",
                             "603", "604", "605", "606", "608", "612", "613", "616", "620",
                             "622", "624", "629", "631", "632", "636", "644", "648", "650",
                             "652", "654", "657", "658", "659", "660", "661", "664", "668",
                             "672", "676", "677", "678", "679", "680", "681", "684", "685",
                             "686", "687", "705", "710", "715", "720", "725", "730", "735",
                             "740", "745", "755", "760", "765", "770", "775", "802", "805",
                             "806", "807", "808", "809", "811", "812", "813", "814", "815",
                             "816", "817", "818", "819", "820", "821", "822", "826", "827",
                             "828", "829", "830", "832", "833", "835", "839", "840", "980",
                             "990"] = field(default=None)
    # Gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHT: Literal["1", "2", "-"] = field(default=None)	
    # Country of birth of persons mother
    GBAGEBOORTELANDMOEDER: Literal["000", "101", "102", "103", "104", "105", "106", "111", "112",
                             "113", "114", "115", "117", "118", "119", "120", "121", "122", 
                             "123", "124", "126", "127", "128", "129", "130", "131", "132",
                             "133", "134", "136", "137", "138", "139", "140", "141", "143",
                             "144", "146", "148", "152", "153", "154", "155", "156", "157",
                             "158", "159", "160", "161", "162", "163", "164", "203", "204",
                             "205", "209", "213", "216", "220", "229", "235", "239", "241",
                             "246", "249", "250", "254", "256", "260", "264", "266", "270",
                             "273", "276", "278", "279", "281", "283", "286", "289", "296",
                             "299", "303", "304", "306", "307", "308", "309", "313", "319",
                             "322", "323", "326", "329", "333", "336", "337", "338", "339",
                             "346", "355", "356", "357", "359", "369", "373", "376", "386",
                             "389", "393", "404", "406", "407", "409", "410", "412", "416",
                             "420", "424", "426", "428", "430", "432", "436", "444", "448", 
                             "452", "456", "460", "464", "476", "478", "480", "484", "488",
                             "492", "496", "500", "502", "504", "508", "510", "512", "513",
                             "516", "520", "524", "528", "534", "537", "540", "544", "548",
                             "550", "552", "554", "564", "568", "575", "578", "601", "602",
                             "603", "604", "605", "606", "608", "612", "613", "616", "620",
                             "622", "624", "629", "631", "632", "636", "644", "648", "650",
                             "652", "654", "657", "658", "659", "660", "661", "664", "668",
                             "672", "676", "677", "678", "679", "680", "681", "684", "685",
                             "686", "687", "705", "710", "715", "720", "725", "730", "735",
                             "740", "745", "755", "760", "765", "770", "775", "802", "805",
                             "806", "807", "808", "809", "811", "812", "813", "814", "815",
                             "816", "817", "818", "819", "820", "821", "822", "826", "827",
                             "828", "829", "830", "832", "833", "835", "839", "840", "980",
                             "990"] = field(default=None)
    # Country of birth of persons father
    GBAGEBOORTELANDVADER: Literal["000", "101", "102", "103", "104", "105", "106", "111", "112",
                             "113", "114", "115", "117", "118", "119", "120", "121", "122", 
                             "123", "124", "126", "127", "128", "129", "130", "131", "132",
                             "133", "134", "136", "137", "138", "139", "140", "141", "143",
                             "144", "146", "148", "152", "153", "154", "155", "156", "157",
                             "158", "159", "160", "161", "162", "163", "164", "203", "204",
                             "205", "209", "213", "216", "220", "229", "235", "239", "241",
                             "246", "249", "250", "254", "256", "260", "264", "266", "270",
                             "273", "276", "278", "279", "281", "283", "286", "289", "296",
                             "299", "303", "304", "306", "307", "308", "309", "313", "319",
                             "322", "323", "326", "329", "333", "336", "337", "338", "339",
                             "346", "355", "356", "357", "359", "369", "373", "376", "386",
                             "389", "393", "404", "406", "407", "409", "410", "412", "416",
                             "420", "424", "426", "428", "430", "432", "436", "444", "448", 
                             "452", "456", "460", "464", "476", "478", "480", "484", "488",
                             "492", "496", "500", "502", "504", "508", "510", "512", "513",
                             "516", "520", "524", "528", "534", "537", "540", "544", "548",
                             "550", "552", "554", "564", "568", "575", "578", "601", "602",
                             "603", "604", "605", "606", "608", "612", "613", "616", "620",
                             "622", "624", "629", "631", "632", "636", "644", "648", "650",
                             "652", "654", "657", "658", "659", "660", "661", "664", "668",
                             "672", "676", "677", "678", "679", "680", "681", "684", "685",
                             "686", "687", "705", "710", "715", "720", "725", "730", "735",
                             "740", "745", "755", "760", "765", "770", "775", "802", "805",
                             "806", "807", "808", "809", "811", "812", "813", "814", "815",
                             "816", "817", "818", "819", "820", "821", "822", "826", "827",
                             "828", "829", "830", "832", "833", "835", "839", "840", "980",
                             "990"] = field(default=None)
    # number of persons parents born outside of the Netherlands
    GBAAANTALOUDERSBUITENLAND: int = field(default=None)	
    # Migration background - CBS definition
    GBAHERKOMSTGROEPERING: Literal["000", "101", "102", "103", "104", "105", "106", "111", "112",
                             "113", "114", "115", "117", "118", "119", "120", "121", "122", 
                             "123", "124", "126", "127", "128", "129", "130", "131", "132",
                             "133", "134", "136", "137", "138", "139", "140", "141", "143",
                             "144", "146", "148", "152", "153", "154", "155", "156", "157",
                             "158", "159", "160", "161", "162", "163", "164", "203", "204",
                             "205", "209", "213", "216", "220", "229", "235", "239", "241",
                             "246", "249", "250", "254", "256", "260", "264", "266", "270",
                             "273", "276", "278", "279", "281", "283", "286", "289", "296",
                             "299", "303", "304", "306", "307", "308", "309", "313", "319",
                             "322", "323", "326", "329", "333", "336", "337", "338", "339",
                             "346", "355", "356", "357", "359", "369", "373", "376", "386",
                             "389", "393", "404", "406", "407", "409", "410", "412", "416",
                             "420", "424", "426", "428", "430", "432", "436", "444", "448", 
                             "452", "456", "460", "464", "476", "478", "480", "484", "488",
                             "492", "496", "500", "502", "504", "508", "510", "512", "513",
                             "516", "520", "524", "528", "534", "537", "540", "544", "548",
                             "550", "552", "554", "564", "568", "575", "578", "601", "602",
                             "603", "604", "605", "606", "608", "612", "613", "616", "620",
                             "622", "624", "629", "631", "632", "636", "644", "648", "650",
                             "652", "654", "657", "658", "659", "660", "661", "664", "668",
                             "672", "676", "677", "678", "679", "680", "681", "684", "685",
                             "686", "687", "705", "710", "715", "720", "725", "730", "735",
                             "740", "745", "755", "760", "765", "770", "775", "802", "805",
                             "806", "807", "808", "809", "811", "812", "813", "814", "815",
                             "816", "817", "818", "819", "820", "821", "822", "826", "827",
                             "828", "829", "830", "832", "833", "835", "839", "840", "980",
                             "990"] = field(default=None)
    # migration background - Dutch native, first generation migrant, or second generation migrant
    # "unknown "-", native (Dutch) "0", first generation migrant "1", second generation migrant "2"
    GBAGENERATIE: Literal["-", "0", "1", "2"] = field(default=None)	
    # Year of birth
    GBAGEBOORTEJAAR: int = field(default=None)
    # Mothers gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTMOEDER: Literal["-", "1", "2"] = field(default=None)	
    # Fathers gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTVADER: Literal["-", "1", "2"] = field(default=None)	
    # Mothers birth year
    GBAGEBOORTEJAARMOEDER: int = field(default=None)	
    # Fathers birth year
    GBAGEBOORTEJAARVADER: int = field(default=None)
    # country of origin (CBS definition) - the country where the person was born 
    # or where parents were born if the person was born in the Netherlands
    GBAHERKOMSTLAND: Literal["000", "101", "102", "103", "104", "105", "106", "111", "112",
                             "113", "114", "115", "117", "118", "119", "120", "121", "122", 
                             "123", "124", "126", "127", "128", "129", "130", "131", "132",
                             "133", "134", "136", "137", "138", "139", "140", "141", "143",
                             "144", "146", "148", "152", "153", "154", "155", "156", "157",
                             "158", "159", "160", "161", "162", "163", "164", "203", "204",
                             "205", "209", "213", "216", "220", "229", "235", "239", "241",
                             "246", "249", "250", "254", "256", "260", "264", "266", "270",
                             "273", "276", "278", "279", "281", "283", "286", "289", "296",
                             "299", "303", "304", "306", "307", "308", "309", "313", "319",
                             "322", "323", "326", "329", "333", "336", "337", "338", "339",
                             "346", "355", "356", "357", "359", "369", "373", "376", "386",
                             "389", "393", "404", "406", "407", "409", "410", "412", "416",
                             "420", "424", "426", "428", "430", "432", "436", "444", "448", 
                             "452", "456", "460", "464", "476", "478", "480", "484", "488",
                             "492", "496", "500", "502", "504", "508", "510", "512", "513",
                             "516", "520", "524", "528", "534", "537", "540", "544", "548",
                             "550", "552", "554", "564", "568", "575", "578", "601", "602",
                             "603", "604", "605", "606", "608", "612", "613", "616", "620",
                             "622", "624", "629", "631", "632", "636", "644", "648", "650",
                             "652", "654", "657", "658", "659", "660", "661", "664", "668",
                             "672", "676", "677", "678", "679", "680", "681", "684", "685",
                             "686", "687", "705", "710", "715", "720", "725", "730", "735",
                             "740", "745", "755", "760", "765", "770", "775", "802", "805",
                             "806", "807", "808", "809", "811", "812", "813", "814", "815",
                             "816", "817", "818", "819", "820", "821", "822", "826", "827",
                             "828", "829", "830", "832", "833", "835", "839", "840", "980",
                             "990"] = field(default=None)
    # Born in the Netherlands or outside: 
    # unknown = "-", "0" - born abroad, "1" - born in the Netherlands
    GBAGEBOORTELANDNL: Literal["-", "0", "1"] = field(default=None)
    # person's birthdate (day of birth = 01 for all)
    birthday: str = field(default=None)
    birthyear: int = field(default=None) # TL added this
    birthmonth = Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)

    ## Education

    # highest level of education in 2020 (with diploma) in 18 categories, 
    # Dutch standard classification of education (SOI)
    # 1111 - primary education gr1-2, 1112 - primary education gr3-8, 
    # 1211 - practical education, 1212 - vmbo-b/k, 1213 - mbo1, 
    # 1221 vmbo-g/t, 1222 - havo, vwo lower level, 2111 - mbo2, 2112 - mbo3, 
    # 2121 - mbo4, 2131 - havo upper school, 2132 - vwo upper school, 
    # 3111 - short hbo, 3112 - hbo bachelors degree, 3113 - wo-bachelor, 
    # 3211 - hbo master, 3212 - wo-master, 3213 - phd
    OPLNIVSOI2021AGG4HBmetNIRWO: Literal["1111", "1112", "1211", "1212", "1213",
                                         "1221", "1222", "2111", "2112", "2121",
                                         "2131", "2132", "3111", "3112", "3113",
                                         "3211", "3212", "3213"] = field(default=None)
    # highest level of education in 2020 (without diploma) in 18 categories, 
    # Dutch standard classification of education (SOI)
    OPLNIVSOI2021AGG4HGmetNIRWO: Literal["1111", "1112", "1211", "1212", "1213",
                                         "1221", "1222", "2111", "2112", "2121",
                                         "2131", "2132", "3111", "3112", "3113",
                                         "3211", "3212", "3213"] = field(default=None)
    # highest level of education in 2020 (with diploma) ISCED classification (2011)
    # 0 - pre-primary education, 1 - primary education, 2 - lower secondary education, 
    # 3 - upper secondary education, 4 - post-secondary non-tertiary education, 
    # 5 - short-cycle tertiary education, 6 - bachelors or equivalent, 
    # 7 - masters or equivalent, 8 - doctorate or equivalent
    OPLNIVSOI2021AGG4HBmetNIRWO_isced: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    # highest level of education in 2020 (without diploma) ISCED classification (2011)
    OPLNIVSOI2021AGG4HGmetNIRWO_isced: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    
    ## SES and employment
    
    # start date of person's socioeconomic category (the last one in 2020)
    AANVSECM: str = field(default=None)
    startyear_ses: int = field(default=None) # TL added this
    startmonth_ses: Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)
    startday_ses: Literal["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", # TL added this
                          "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
                          "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    # socio-economic category (the last one in 2020)
    # 11 employee, 12 - director-major shareholder (directeur-grootaandeelhouder), 
    # 13 - entrepreneur (zelfstandig ondernemer), 14 - self-employed, 
    # 15 -contributing family member (meerwerkend gezinslid), 
    # 21 - recipient of unemployment benefit, 22 - recipient of social security benefit, 
    # 23 - recipient of other social security benefit, 24 - recipient of sicness/AO benefit, 
    # 25 - recipient of pension benefit,   26 - studing with income,  
    # 31 - studying without income,  32 - other without income
    SECM: Literal["11", "12", "13", "14", "15", "21", "22", "23", "24", "25", "26", "31", "32"] = field(default=None)
    # number of jobs person did in 2020
    n_jobs: int = field(default=None)
    # number of full-time jobs in 2020
    n_full: int = field(default=None)
    # number of part-time jobs in 2020
    n_part: int = field(default=None)
    # number of jobs with permanent contract in 2020
    n_permanent: int = field(default=None)
    # number of jobs with temporary contract in 2020
    n_temporary: int = field(default=None)
    # number of months worked in 2020 at the main job (the job with most hours)
    n_months_main: int = field(default=None)
    # average hours per month on the main job
    average_hours_main: float = field(default=None)
    # type of contract at the main job (temporary or permanent)
    # O - permanent, B - temporary, N - does not apply
    SCONTRACTSOORT_main: Literal["O", "B", "N"] = field(default=None)
    # whether main job is full-time or part-time: 1 - full-time, 2 - part-time
    SPOLISDIENSTVERBAND_main: Literal["1", "2"] = field(default=None)
    
    ## Marriages/partnerships

    # total number of marriages before 2021
    marriages_total: int = field(default=None)
    # total number of partnerships before 2021
    partnerships_total: int = field(default=None)
    # civil status at the end of 2020
    # H - married, O - unmarried, P - registered partnership, S - divorced after parriage, 
    # SP  - divorced after registered partnership,  W - widowed after marriage, 
    # WP - widowed after registered partnership
    GBABURGERLIJKESTAATNW: Literal["H", "O", "P", "S", "SP", "W", "WP"] = field(default=None)
    # start date of the civil status at the end of 2020 (e.g. date of marriage if married or divorce if divorced)
    AANVANGVERBINTENIS: str = field(default=None)
    startyear_civilstatus: int = field(default=None) # TL added this
    startmonth_civilstatus: Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)
    startday_civilstatus: Literal["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", # TL added this
                          "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
                          "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    # first part of partners ID (RINPERSOONS): R - person is in the Personal records database
    RINPERSOONSVERBINTENISP: str = field(default=None)
    # second part of partners ID (RINPERSOON)
    RINPERSOONVERBINTENISP: str = field(default=None)
    # partners year of birth
    GBAGEBOORTEJAARPARTNER: int = field(default=None)
    # partners month of birth
    GBAGEBOORTEMAANDPARTNER: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] = field(default=None)
    # partners country of birth
    GBAGEBOORTELANDPARTNER: Literal["000", "101", "102", "103", "104", "105", "106", "111", "112",
                             "113", "114", "115", "117", "118", "119", "120", "121", "122", 
                             "123", "124", "126", "127", "128", "129", "130", "131", "132",
                             "133", "134", "136", "137", "138", "139", "140", "141", "143",
                             "144", "146", "148", "152", "153", "154", "155", "156", "157",
                             "158", "159", "160", "161", "162", "163", "164", "203", "204",
                             "205", "209", "213", "216", "220", "229", "235", "239", "241",
                             "246", "249", "250", "254", "256", "260", "264", "266", "270",
                             "273", "276", "278", "279", "281", "283", "286", "289", "296",
                             "299", "303", "304", "306", "307", "308", "309", "313", "319",
                             "322", "323", "326", "329", "333", "336", "337", "338", "339",
                             "346", "355", "356", "357", "359", "369", "373", "376", "386",
                             "389", "393", "404", "406", "407", "409", "410", "412", "416",
                             "420", "424", "426", "428", "430", "432", "436", "444", "448", 
                             "452", "456", "460", "464", "476", "478", "480", "484", "488",
                             "492", "496", "500", "502", "504", "508", "510", "512", "513",
                             "516", "520", "524", "528", "534", "537", "540", "544", "548",
                             "550", "552", "554", "564", "568", "575", "578", "601", "602",
                             "603", "604", "605", "606", "608", "612", "613", "616", "620",
                             "622", "624", "629", "631", "632", "636", "644", "648", "650",
                             "652", "654", "657", "658", "659", "660", "661", "664", "668",
                             "672", "676", "677", "678", "679", "680", "681", "684", "685",
                             "686", "687", "705", "710", "715", "720", "725", "730", "735",
                             "740", "745", "755", "760", "765", "770", "775", "802", "805",
                             "806", "807", "808", "809", "811", "812", "813", "814", "815",
                             "816", "817", "818", "819", "820", "821", "822", "826", "827",
                             "828", "829", "830", "832", "833", "835", "839", "840", "980",
                             "990"] = field(default=None)
    # partners gender: 1 - man, 2 - woman, "-" - unknown
    GBAGESLACHTPARTNER: Literal["-", "1", "2"] = field(default=None)
    # partners highest level of education in 2020 (with diploma) in 18 categories, Dutch standard classification of education (SOI)
    OPLNIVSOI2021AGG4HBmetNIRWO_partner: Literal["1111", "1112", "1211", "1212", "1213",
                                         "1221", "1222", "2111", "2112", "2121",
                                         "2131", "2132", "3111", "3112", "3113",
                                         "3211", "3212", "3213"] = field(default=None)	
    # partners highest level of education in 2020 (without diploma), Dutch standard classification of education (SOI)
    OPLNIVSOI2021AGG4HGmetNIRWO_partner: Literal["1111", "1112", "1211", "1212", "1213",
                                         "1221", "1222", "2111", "2112", "2121",
                                         "2131", "2132", "3111", "3112", "3113",
                                         "3211", "3212", "3213"] = field(default=None)
    # partners highest level of education in 2020 (with diploma) ISCED classification (2011)
    OPLNIVSOI2021AGG4HBmetNIRWO_partner_isced: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    # partners highest level of education in 2020 (without diploma) ISCED classification (2011)
    OPLNIVSOI2021AGG4HGmetNIRWO_partner_isced: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    # start date of partner's socioeconomic category (the last one in 2020)
    AANVSECM_partner: str = field(default=None)
    startyear_partnerses: int = field(default=None) # TL added this
    startmonth_partnerses: Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)
    startday_partnerses: Literal["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", # TL added this
                          "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
                          "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    # partner's socio-economic category in 2020
    SECM_partner: Literal["11", "12", "13", "14", "15", "21", "22", "23", "24", "25", "26", "31", "32"] = field(default=None)
    
    ## Income
    
    # persons taxable income in 2020
    INPBELI: float = field(default=None)
    # economic independence of the person in 2020
    # 0 - not economically independent, 1 - economically independent, 
    # 8 - does not belong to the target population of economic independence, 
    # 9 - does not belong to private households with observed income
    INPEMEZ: Literal["0", "1", "8", "9"] = field(default=None)
    # financial independence of the person (being able to survive on ones own income) in 2020
    # 0 - not financially independent, 1 - financially independent, 
    # 8 - does not belong to the target population of financial independence, 
    # 9 - does not belong to private households with observed income
    INPEMFO: Literal["0", "1", "8", "9"] = field(default=None)
    # percentile groups of personal gross income of persons with income in private households in 2020
    # '-3' - persons in institutional households, 
    # '-2' - persons in private households with unknown income, 
    # '-1' - persons without personal income
    INPP100PBRUT: int = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # percentile groups of personal income of persons with income in private households in 2020
    # '-3' - persons in institutional households, 
    # '-2' - persons in private households with unknown income, 
    # '-1' - persons without personal income
    INPP100PPERS: int = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # personal primary income in 2020
    INPPERSPRIM: float = field(default=None)
    # whether the person has personal income in 2020
    # 0 - without personal income, 1 - with personal income, 
    # 9 - person belongs to a household with unknown income
    INPPINK: Literal["0", "1", "8", "9"] = field(default=None)
    # position of the person in relation to the main breadwinner in the household in 2020
    # 1 - main breadwinner without partner, 2 - main breadwinner with partner, 
    # 3 - married martner, 4 - unmarried partner, 5 - minor child, 
    # 6 - adult child (18 years old or older), 7 - other household member, 8 - household unknown
    INPPOSHHK: Literal["1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    # together with RINPERSOONHKW identifies the breadwinner in the household - to link households income and wealth to individuals
    RINPERSOONSHKW: str = field(default=None)
    # together with RINPERSOONSHKW identifies the breadwinner in the household - to link households income and wealth to individuals
    RINPERSOONHKW: str = field(default=None)
    # number of people in the household in 2020
    INHAHL: int = field(default=None)
    # number of people with personal income in the household in 2020
    INHAHLMI: int = field(default=None)
    # household income in 2020 relative to the European poverty line in 2020
    # -2' - institutional household, '-1' - private household with unknown income
    INHARMEUR: float = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # household income in 2020 relative to the European poverty line in the last 4 years  (2017-2020)
    # -4'- no target population in at least 2 of the previous 3 years, 
    # '-2' - institutional household, '-1' - private household with unknown income
    INHARMEURL: float = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # main source of the households income in 2020
    # 99 - household income unknown, 11 - wage, 12 - salary director-major shareholder, 
    # 13 - profit independent entrepreneur, 14 - income other self-employed, 
    # 21 - unemployment benefits, 22 - social security benefit, 
    # 23 - other social security benefits, 24 - sickness/disability benefit, 
    # 25 - pension benefits, 26 - student grants, 30 - property income
    INHBBIHJ: Literal["99", "11", "12", "13", "14", "21", "22", "23", "24", "25", "26", "30"] = field(default=None)
    # gross households income in 2020
    INHBRUTINKH: float = field(default=None)
   
    ## Wealth, assets, benefits

    # type of home ownership of the household on January 1 2020 based on whether the household owns or rents a home 
    # and whether the household receives rent benefit
    # 1 - own house, 2 - rental house without rent allowance, 3 - rental house with rent allowance, 
    # 8 - institutional household, 9 - unknown household
    INHEHALGR: Literal["1", "2", "3", "8", "9"] = field(default=None)
    # type of household depending on whether a household has income in 2020
    # 1 - private household with income (not a student household), 
    # 2 - private students household with income, 3 - institutional household with income, 
    # 7 - private household without income, 8 - institutional outcome without income, 
    # 9 - private but does not belong to household population (persons not classified) 
    INHPOPIIV: Literal["1", "2", "3", "7", "8", "9"] = field(default=None)
    # type of household depending on number of members of pension age in 2020
    # 11 - single man of state pension age, 12 - single woman of state pension age, 
    # 13 - (married) couple, both partners of state pension age, 
    # 14 - (married) couple, one partner of state pension age, 
    # 15 - other multiple-persons household with at least one member of state pension age, 
    # 20 - household in IIT, at least one person from state pension age, 
    # 31 - single person up to state pension age, 
    # 32 - multi-person household, all people up to state pension age, 88 - unknown household
    INHSAMAOW: Literal["11", "13", "14", "15", "20", "31", "32", "88"] = field(default=None)
    # household composition depending on the mutual relationships of people in the household and their gender and age in 2020
    # 11 - single-person household, man up to state pension age, 
    # 12 - single-person household, man of state pension age, 
    # 13 - single-person household, woman up to state pension age, 
    # 14 - single-person household, woman of state pension age, 
    # 21 - couple without children, main breadwinner up to state pension age, 
    # 22 - couple without children, main breadwinner of state pension age, 
    # 31 - couple with only underage children (under 18 years old), 
    # 32 - couple with underage children (under 18 years old) and children aged 18 years or older, 
    # 33 - couple with only children aged 18 years or older, 
    # 41 - single-parent family with only underage children (under 18 years old), 
    # 42 - single-parent family with underage children (under 18 years old) and children aged 18 years or older, 
    # 43 - single-parent family with only children from 18 years or older, 
    # 51 - couple without children but with other resident(s), 
    # 52 - couple with underage children and other resident(s), 
    # 53 - couple with underage children and children aged 18 years or older and other resident(s), 
    # 54 - couple with only children aged 18 or older and other resident(s), 
    # 55 - single-parent family with only underage children (under 18 years old) and other resident(s), 
    # 56 - single-parent family with underage children (under 18 years old) and children aged 18 years or older and other resident(s), 
    # 57 - single-parent family with only children aged 18 years or older and other resident(s), 
    # 58 - other multi-person household, 71 - people living in institutions (nursing homes, care homes, rehabilitation centers, penitentiary institutions, children's homes), 
    # 88 - unknown household  
    INHSAMHH: Literal["11", "12", "13", "14", "21", "22", "31", "32", "33", "41", "42", "43",
                      "51", "52", "53", "54", "55", "56", "57", "58", "88"] = field(default=None)
    # degree of benefit dependence of the household in 2020
    # -2' - institutional household, '-1' - private household with unknown income, 
    # 0 - 0%, no benefits
    INHUAF: int = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # degree of benefit dependence of the household in the last 4 years (2017-2020)
    # -4' - no target population in at least one of the previous 3 years, 
    # '-2' - institutional household, '-1' - private household with unknown income, 
    # 0 - 0%, no benefits
    INHUAFL: int = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # main benefit of the household in 2020
    # 0 - no benefit, 1 - unemployment benefit, 2 - disability benefit, 
    # 3 - social security benefit, 4 - other social security benefits, 
    # 8 - institutional household, 9 - private household with unknown income
    INHUAFTYP: Literal["0", "1", "2", "3", "4", "8", "9"] = field(default=None)
    # percentile groups of private households based on assets and income in 2020
    # -1' - private household with an unknown income/assets, '-2' - institutional household
    VEHP100WELVAART: int = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # percentile group of the households based on assets in 2020
    # -1' - private household with an unknown income/assets, '-2' - institutional household
    VEHP100HVERM: int = field(default=None) ## TODO: when making feature dict, need to convert these negative numbers to retain their meaning
    # household wealth - difference between assets and debts in 2020
    VEHW1000VERH: float = field(default=None)
    # total assets in 2020 - total value of bank and savings deposits and securities, 
    # bonds and shares, owner-occupied home, business assets and other assets of a household
    VEHW1100BEZH: float = field(default=None)
    # household finantial assets in 2020 - bank and savings deposits and securities
    VEHW1110FINH: float = field(default=None)
    # households real estate assets in 2020 - total value of owner-occupied home and other real estate
    VEHW1120ONRH: float = field(default=None)
    # households business assets in 2020
    VEHW1130ONDH: float = field(default=None)
    # value of a substantial interest of a household (substantial interest is a share 
    # of at least 5 percent in the issued capital of a company) in 2020
    VEHW1140ABEH: float = field(default=None)
    # total value of other households assets in 2020
    VEHW1150OVEH: float = field(default=None)
    # total value of households debts in 2020
    VEHW1200STOH: float = field(default=None)
    # mortgage debt for owner-occupied home of the household  in 2020
    VEHW1210SHYH: float = field(default=None)
    # households student debts in 2020
    VEHW1220SSTH: float = field(default=None)
    # other households debts in 2020
    VEHW1230SOVH: float = field(default=None)
    # households assets excluding own home in 2020
    VEHWVEREXEWH: float = field(default=None)

    ## Location, childcare amenities

    # start date of address where the person lives at the end of 2020
    GBADATUMAANVANGADRESHOUDING: str = field(default=None)
    startyear_address: int = field(default=None) # TL added this
    startmonth_address: Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)
    startday_address: Literal["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", # TL added this
                          "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
                          "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    # ID of persons address at the end of 2020
    SOORTOBJECTNUMMER: str = field(default=None)	
    # second part of ID of persons address at the end of 2020
    RINOBJECTNUMMER: str = field(default=None)
    # Distance in meters from address to the nearest daycare center (calculated by road)
    VZAFSTANDKDV: float = field(default=None)
    # Number of daycare centers within 1 km from address
    VZAANTKDV01KM: int = field(default=None)
    # Number of daycare centers within 3 km from address
    VZAANTKDV03KM: int = field(default=None)
    # Number of daycare centers within 5 km from address
    VZAANTKDV05KM: int = field(default=None)
    # Distance in meters from address to the nearest after-school care (calculated by road)
    VZAFSTANDBSO: float = field(default=None)
    # Number of after-school care centers within 1 km from address
    VZAANTBSO01KM: int = field(default=None)
    # Number of after-school care centers within 3 km from address
    VZAANTBSO03KM: int = field(default=None)
    # Number of after-school care centers within 5 km from address
    VZAANTBSO05KM: int = field(default=None)

    ## Household info

    # type of residential object (housing type)
    # 01' - detached house, '02' - semi-detached house, '03' - corner house, 
    # '04' - terraced house, '05' - multi-family house, '99' -  unknown
    VBOWoningtype: Literal["01", "02", "03", "04", "05", "99"] = field(default=None)
    # start date of the last household the person belonged to in 2020
    DATUMAANVANGHH: str = field(default=None)
    startyear_household: int = field(default=None) # TL added this
    startmonth_household: Literal["01", "02", "03", "04", "05", "06", "07", # TL added this
                                 "08", "09", "10", "11", "12"] = field(default=None)
    startday_household: Literal["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", # TL added this
                          "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
                          "24", "25", "26", "27", "28", "29", "30", "31"] = field(default=None)
    # household id in 2020 (the last one in 2020)
    HUISHOUDNR: str = field(default=None)
    # type of the household (the last one in 2020) based on relationships between people in the household
    # 1 - single-member household, 2 - unmarried couple without children, 
    # 3 - married couple without children, 4 - unmrried couple with children, 
    # 5 - married couple with children, 6 - single-parent household, 7 - other household, 
    # 8 - institutional household
    TYPHH: Literal["1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    # number of people in the household (the last one in 2020)
    AANTALPERSHH: int = field(default=None)
    # number of people in the household with position 'other' (for the last household in 2020)
    AANTALOVHH: int = field(default=None)
    # year of birth of the youngest child in the household (including stepchildren) (for the last household in 2020)
    GEBJAARJONGSTEKINDHH: str = field(default=None)
    

    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name == 'lisa_tab', "This class is specifically designed for the Lisa base dataset. Dataset name must be 'lisa_tab'"

        ## wrangle constructed date variables
        
        # birthday of youngest child
        if len(self.birthday_youngest) == 8: # to ensure that date string is in YYYYMMDD format
            self.birthyear_youngest = self.birthday_youngest[:4].astype(int)
            self.birthmonth_youngest = self.birthday_youngest[4:6]

        # own birthday
        if len(self.birthday) == 8:
            self.birthyear = self.birthday[:4].astype(int)
            self.birthmonth = self.birthyear[4:6]

        # start date of own SES category
        if len(self.AANVSECM) == 8:
            self.startyear_ses = self.AANVSECM[:4].astype(int)
            self.startmonth_ses = self.AANVSECM[4:6]
            self.startday_ses = self.AANVSECM[6:8]

        # start date of civil status
        if len(self.ANVANGVERBINTENIS) == 8:
            self.startyear_civilstatus = self.AANVANGVERBINTENIS[:4].astype(int)
            self.startmonth_civilstatus = self.AANVANGVERBINTENIS[4:6]
            self.startday_civilstatus = self.AANVANGVERBINTENIS[6:8]

        # start date of partner's SES category
        if len(self.AANVSECM_partner) == 8:
            self.startyear_partnerses = self.AANVSECM_partner[:4].astype(int)
            self.startmonth_partnerses = self.AANVSECM_partner[4:6]
            self.startday_partnerses = self.AANVSECM_partner[6:8]

        # start date of current address
        if len(self.GBADATUMAANVANGADRESHOUDING) == 8:
            self.startyear_address = self.GBADATUMAANVANGADRESHOUDING[:4].astype(int)
            self.startmonth_address = self.GBADATUMAANVANGADRESHOUDING[4:6]
            self.startday_address = self.GBADATUMAANVANGADRESHOUDING[6:8]

        # start day of household
        if len(self.DATUMAANVANGHH) == 8:
            self.startyear_household = self.DATUMAANVANGHH[:4].astype(int)
            self.startmonth_household = self.DATUMAANVANGHH[4:6]
            self.startday_household = self.DATUMAANVANGHH[6:8]


    def get_paragraph_string_biographic(self, features=None):
        pass