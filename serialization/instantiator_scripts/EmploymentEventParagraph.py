from dataclasses import dataclass, field, fields
from typing import Literal
from serialization.instantiator_scripts.Paragraph import Paragraph

@dataclass
class EmploymentEventParagraph(Paragraph):
    """
    The EmploymentEventParagraph class is designed for the dataset that includes employment information
    on jobs and wages of employees at Dutch companies for a given reporting year.
    It includes attributes such as start and end dates of the reporting period, wages, benefits, insurance,
    etc. 
    name: employment_bus
    """

# Imputation
    ## Whether record was imputed at all
    SIMPUTATIE: Literal["J", "N", "-"] = field(default=None)
    ## Whether record was a complete imputation or not (0 = complete imputation)
    SINDWAARNEMING: Literal["0", "1"] = field(default=None)

# Dates, times, reporting periods
    ## Date of start of income statement/reporting period
    SDATUMAANVANGIKO: str = field(default=None)
    ## Date of start of income relationship/reporting period (unclear how this is diff from above)
    SDATUMAANVANGIKV: str = field(default=None)
    ## Original start date of income relationship as stated in wage tax return
    SDATUMAANVANGIKVORG: str = field(default=None)
    ## Date of end of income statement/reporting period
    SDATUMEINDEIKO: str = field(default=None)
    ## Date of end of income relationship/reporting period (again unclear how this is diff from above)
    SDATUMEINDEIKV: str = field(default=None)
    ## Number of calendar days that the job exists
    SBAANDAGEN: int = field(default=None)
    ## Number of full time days
    SVOLTIJDDAGEN: int = field(default=None)
    ## Number of days in which wages were received
    SAANTSV: int = field(default=None)
    ## Number of regular working hours
    SREGULIEREUREN: int = field(default=None)
    ## Class of weekly working hours 
    ## 1: <12 hrs, 2: 12-20 hrs, 3: 20-25 hrs, 4: 25-30, 5: 30-35, 6: 35+
    SWEKARBDUURKLASSE: Literal["1", "2", "3", "4", "5", "6"] = field(default=None)
    ## Number of contract hours per week
    SAANTCTRCTURENPWK: int = field(default=None)
    ## Number of hours paid
    SAANTVERLU: int = field(default=None)
    ## Number of paid hours minus overtime hours
    SBASISUREN: int = field(default=None)
    ## Number of additional hours worked for a higher hourly wage
    SOVERWERKUREN: int = field(default=None)
    ## Phase in which income relationship is in the context of Flexibility and Security Act
    SFSINDFZ: Literal["--", "00", "01", "02", "03", "04", "05", "06", "17", "18",
                      "19", "38", "40", "41", "42", "43", "44"] = field(default=None)
    ## Period for which wage tax returns are submitted
    ## 1: four-week assignment, 3: half-yearly assignment, 4: annual, 5: monthly
    STIJDVAKTYPE: Literal["1", "3", "4", "5"] = field(default=None)
    
# Employment info
    ## Type of employment (1 = full-time, 2 = part-time)
    SPOLISDIENSTVERBAND: Literal["1", "2"] = field(default=None)
    ## Permanent or flexible employment
    SARBEIDSRELATIE: Literal["1", "2"] = field(default=None)
    ## Code for whether employee worked overtime
    SOVERWERK: Literal["0", "1"] = field(default=None)
    ## Code for whether is a public law appointment for indefinite period
    INDPUBAANONBEPTD: Literal["J", "N"] = field(default=None)

# Employer info
    ## Statistical unit of the company as recorded in General Company Register (ABR)
    SBEID: str = field(default=None)
    ## Code for collective labor agreement sector of company
    SCAOSECTOR: Literal["1000", "2000", "3000", "3100", "3200", "3210", "3211",
                        "3212", "3213", "3220", "3230", "3240", "3250", "3290",
                        "3300", "3310", "3320", "3400", "3500", "3600", "3700",
                        "3800"] = field(default=None)
    ## Sector code
    SSECT: Literal["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                   "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                   "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                   "30", "31", "32", "33", "34", "35", "38", "39", "40", "41",
                   "42", "43", "44", "45", "46", "47", "48", "49", "50", "51",
                   "52", "53", "54", "55", "56", "57", "58", "59", "60", "61",
                   "62", "63", "64", "65", "66", "67", "68", "69", "99"] = field(default=None)
    ## Job type code
    SSOORTBAAN: Literal["1", "2", "3", "4", "5", "9"] = field(default=None)
    ## Amount of employer's tax Zvw
    SWGHZVW: float = field(default=None)
    ## Amount of employer's low AWf premium
    PrAwfLg: float = field(default=None)
    ## Amount of employer's high AWf premium
    PrAwfHg: float = field(default=None)
    ## Amount of employer's revised AWf premium
    PrAwfHz: float = field(default=None)
    
# Wage information
    ## Amount of basic salary (excluding special rewards, allowances, overtime)
    SBASISLOON: float = field(default=None)
    ## Contract wages
    SCTRCTLN: float = field(default=None)
    ## Code for income relationship type
    SSRTIV: Literal["11", "12", "13", "14", "15", "17", "18", "21", "22", "23",
                    "24", "31", "32"] = field(default=None)
    ## Amount paid as incidental salary
    SINCIDENTSAL: float = field(default=None)
    ## Code for incidental income reduction (reason why wage temporarily lower than agreed wage)
    SCDINCINKVERM: Literal["--", "B", "G", "O", "S", "Z"] = field(default=None)
    ## Total amount of wages in money
    SLNINGLD: float = field(default=None)
    ## Value of wages that aren't paid in cash (from which tax / premiums must be paid)
    SWRDLN: float = field(default=None)
    ## Increase in cumulative UFO premium wage
    PRLNUFO: float = field(default=None)
    ## Increase in cumulative low AWf premium wage
    PRLNAWFANWLg: float = field(default=None)
    ## Increase in cumulative high AWf premium wage
    PRLNAWFANWHg: float = field(default=None)
    ## Increase in cumulative revised AWf premium wage
    PRLNAWFANWHz: float = field(default=None)
    ## Amount over which high Disability Fund premium is calculated
    PRLNAOFANWHG: float = field(default=None)
    ## Amount over which low Disability Fund premium is calculated
    PRLNAOFANWLG: float = field(default=None)
    ## Amount over which cumulative premium wage Disability Fund is calculated
    PRLNAOFANWUIT: float = field(default=None)

# Insurance-related info
    ## Whether has insurance under WAO/WIA
    SINDWAO: Literal["N", "J"] = field(default=None)
    ## Whether has insurance under WW
    SINDWW: Literal["N", "J"] = field(default=None)
    ## Wage that is used to determine premiums for employee insurance
    SLNSV: float = field(default=None)
    ## Code for risk premium group for which sector fund premium is calculated
    SRISGRP: Literal["--", "00", "01", "02", "03", "04", "05", "06", "07", "08",
                     "09", "10", "11"] = field(default=None)
    ## Amount of wages withheld due to payroll tax and national insurance contributions
    SINGLBPH: float = field(default=None)
    ## Wages on which payroll tax + national insurance contributions are calculated
    SLNLBPH: float = field(default=None)
    ## First code for what special circumstance influenced the employee insurance obligation
    SCDINVLVPL1: Literal["--", "A", "B", "C", "D", "E", "F", "X"] = field(default=None)
    ## Second code for what special circumstance influenced the employee insurance obligation
    SCDINVLVPL2: Literal["--", "A", "B", "C", "D", "E", "F", "X"] = field(default=None)
    ## Third code for what special circumstance influenced the employee insurance obligation
    SCDINVLVPL3: Literal["--", "A", "B", "C", "D", "E", "F", "X"] = field(default=None)
    ## Amount paid to employee as supplement to employee insurance benefit
    SVERSTRAANV: float = field(default=None)
    ## Amount reimbursed to employee with withheld contribution under Zvw (Health Insurance Act)
    SVERGZVW: float = field(default=None)

# Wage deductions
    ## Amount of tax-free deductions
    SPENSIOENPREMIE: float = field(default=None)
    ## Amount of wages deducted due to sea days
    SBEDRZDAFTR: float = field(default=None)
    ## Amount of wages withheld as a Zvw contribution (Health Insurance Act)
    SBIJDRZVW: float = field(default=None)
    ## Payroll tax table code used for withholding payroll tax / national insurance contributions
    SLBTAB: Literal["620", "621", "622", "623", "624", "625", "710", "711", "712", "713", "714", 
                    "715", "720", "721", "722", "723", "724", "725", "940", "950", "998", "999", "010", "011", 
                    "012", "013", "014", "015", "020", "021", "022", "023", "024", "025", "210", "220", "221", 
                    "224", "225", "226", "227", "228", "250", "310", "311", "312", "313", "314", "315", "320", 
                    "321", "322", "323", "324", "325", "510", "511", "512", "513", "514", "515", "520", "521", 
                    "522", "523", "524", "525", "610", "611", "612", "613", "614", "615", "252"] = field(default=None)
    ## Encrypted payroll tax number
    SLHNR_crypt: str = field(default=None)
    ## Insurance situation code (Zxw)
    SCDZVW: Literal["-", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                    "M", "N"] = field(default=None)
    ## Amount deducted from social assistance benefit in connection to alimony
    ## (alimony paid directly)
    SBEDRRCHTAL: float = field(default=None)
    ## Amount of alimony included in social assistance benefit
    ## only applies for Participation Act (2015 onward), WWB (up to 2014),
    ## WIJ (2009-2011)
    SBEDRALINWWB: float = field(default=None)
    ## Amount of wages that's taxed according to special rewards table
    SLNTABBB: float = field(default=None)

# Credits/benefits in addition to wages
    ## Amount reimbursed for travel expenses
    SREISK: float = field(default=None)
    ## Amount of employer contribution to childcare costs
    ## discontinued from 2008 onward
    SWGBIJDRKO: float = field(default=None)
    ## Amount that employer must pay to childcare surcharge
    OPSLWKO: float = field(default=None)
    ## Accrual of employment conditions amount (future wage component)
    OPBAVWB: float = field(default=None)
    ## Amount of future wage component that's not a separate accrual that's accrued
    OPNAVWB: float = field(default=None)
    ## Amount of future wage component that's not a separate accrual that is paid out
    OPNAVWB: float = field(default=None)
    ## Amount that employer pays for the high Disability Fund premium
    PRAOFHG: float = field(default=None)
    ## Amount that employer pays for the low Disability Fund premium
    PRAOFLG: float = field(default=None)
    ## Amount that employer pays for Disability Fund premium (WW, ZW, WIA, etc.)
    PRAOFUIT: float = field(default=None)
    ## Whether has company car
    SAUTOVANDEZAAK: Literal["0", "1"] = field(default=None)
    ## Value of private use of car
    SWRDPRGEBRAUT: float = field(default=None)
    ## Amount of addition to a wage for private use of company car
    SAUTOZAAK: float = field(default=None)
    ## Amount of employee's own contribution for private use of company car
    SWRKNBIJDRAUT: float = field(default=None)
    ## Code for reason why no additional charge for private use of company car
    SCDRDNGNBIJT: Literal["-", "0", "1", "2", "3", "4", "5", "6", "7", "8"] = field(default=None)
    ## Amount of special reward not paid regularly (e.g., performance rewards, bonuses)
    SBIJZONDEREBELONING: float = field(default=None)
    ## Amount paid to employee in addition to salary as part of employment contract
    SEXTRSAL: float = field(default=None)
    ## Total amount paid in wages because of overtime
    SLNOWRK: float = field(default=None)
    ## Amount saved by employee in life-course savings scheme
    SLVLPREG: float = field(default=None)
    ## Amount applied to life-course leave discount (part of tax credits)
    ## dicontinued from 2022 onward
    SLVLPREGTOEG: float = field(default=None)
    ## Amount of settled employment tax credit
    SVERRARBKRT: float = field(default=None)
    ## Whether temporary tax credit was applied
    SINDTIJDHK: Literal["J", "N", "-"] = field(default=None)
    ## Value of accrued right to compensation for additional salary period
    SOPGRCHTEXTRSAL: float = field(default=None)
    ## Amount paid to employee in holiday allowance
    SVAKBSL: float = field(default=None)
    ## Value of accrued right to holiday allowance
    SOPGRCHTVAKBSL: float = field(default=None)
    ## Amount of interest and/or cost benefit on personnel loan
    SBEDRRNTKSTVPERSL: float = field(default=None)
    ## Amount of premium for the employee contribution to pension scheme
    SModelramingPensioenpremieWn: float = field(default=None)
    ## Amount of premium for the employer contribution to pension scheme
    SModelramingPensioenpremieWg: float = field(default=None)
    ## Amount of employee contribution to early retirement scheme
    SModelramingVutpremieWn: float = field(default=None)
    ## Amount of employer contribution to early retirement scheme
    SModelramingVutpremieWg: float = field(default=None)
    ## Amount of employer contribution to social fund
    SModelramingSFpremieWg: float = field(default=None)

# Code classifications for employee credits/benefits
    ## Code for whether employee provided transport to employee
    SINDSA03: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether payroll tax credit was applied
    SINDLHKORT: Literal["J", "N"] = field(default=None)
    ## Code for whether a staff loan was taken out for which interest/cost benefits not part of wages
    SINDSA43: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether wages consist of AOW and/or AIO benefit for single persons
    SINDSA71: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether wages include Wajong benefit
    SINDSA72: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether holiday vouchers or time saving schemes were applied
    SINDVAKBN: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether employee insured under the ZW sickness benefits act
    SINDZW: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether employee received contributions to life-course savings scheme
    SINLEGLEVENSLOOP: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether time savings fund/scheme was applied
    INDDEELNTIJDSPF: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether premium discount for younger employees was applied
    SINDPRKJONGRWEN: Literal["J", "N", "-"] = field(default=None)
    ## Code for whether premium discount for older employees was applied
    SINDPKNWARBVOUDWN: Literal["-", "J", "N"] = field(default=None)
    ## Code for whether premium discount for disabled employee was applied
    SINDPKAGH: Literal["-", "A", "B", "C", "J", "N"] = field(default=None)
    ## Code for whether premium exemption for marginal work was applied
    SINDPMA: Literal["J", "N"] = field(default=None)
    ## Code for whether employer requested eligibility for wage cost benefit for older employee
    SIndAvrLkvOudrWn: Literal["J", "N"] = field(default=None)
    ## Code for whether employer requested eligibility for wage cost benefit for disabled employee
    SIndAvrLkvAgWn: Literal["J", "N", "-"] = field(default=None)
    ## Code for whether eligibility for wage cost benefit was requested for target group of job/ed obstacles
    SIndAvrLkvDgBafSb: Literal["J", "N", "-"] = field(default=None)
    ## Code for whether wage cost benefit eligibility was requested to relocate disabled employee
    SIndAvrLkvHpAgWn: Literal["J", "N", "-"] = field(default=None)
    ## Code for reason fro ending employment 
    CdRdnEindArbov: Literal["01", "02", "03", "04", "05", "06", "20", "21", "30", "31",
                            "40", "41", "50", "51", "90", "91", "92", "99"] = field(default=None)

# Money admin unit owes during the reporting period
    ## Amount owed for WW Awf premium
    SPRAWF: float = field(default=None)
    ## Amount owed to Ufo (Government Implementation Fund)
    SPRUFO: float = field(default=None)
    ## Amount owed for basic premium for disability insurance (WAO/IVA/WGA)
    SPRWAOAOF: float = field(default=None)
    ## Amount owed for WAO or WGA premium (disability insurance)
    SPRWAOAOK: float = field(default=None)
    ## Amount of differentiated WGA premium
    SPRWGAWHK: float = field(default=None)
    ## Amount of differentiated premium Whk (resumption of work fund)
    SPRGEDIFFWHK: float = field(default=None)
    ## Amount over which Whk premium was calculated 
    PRLNWHKANW: float = field(default=None)
    ## Amount for which AWf benefit premium paid by the adminstrative unit
    PRLNAWFANWUIT: float = field(default=None)
    ## Amount owed for AWf premium
    PRAWFUIT: float = field(default=None)
    ## Code for applicable disability discount
    SCDAGH: Literal["--", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] = field(default=None)
    ## Amount owed to employee insurance sector fund
    SPRWGF: float = field(default=None)

# Type of employee/employer relationship
    ## Type of employee contract
    SCONTRACTSOORT: Literal["B", "O", "N"] = field(default=None)
    ## Code for collective labor agreement that applies to the employee
    SCAO_crypt: str = field(default=None)
    ## Code for nature of employment relationship (used for employee insurance)
    ## these codes have changed over time so may not be comparable across yrs
    SCDAARD: Literal["--", "01", "02", "03", "04", "05", "06", "07", "08",
                     "09", "10", "11", "12", "13", "14", "17", "18", "19",
                     "78", "79", "80", "81", "82", "83", "99", "00"] = field(default=None)
    ## Encrypted code of collective labor agreement 
    CdCaoInl_crypt: str = field(default=None)
    ## Code for whether employment contract is for an indefinite period
    IndArbovOnbepTd: Literal["J", "N"] = field(default=None)
    ## Code for whether employment contract is recorded in writing
    IndSchriftArbov: Literal["J", "N"] = field(default=None)
    ## Code for whether there is an on-call agreement
    IndOprov: Literal["J", "N"] = field(default=None)
    ## Code for whether annual hours standard has been applied
    IndJrurennrm: Literal["J", "N"] = field(default=None)


    
    def __post_init__(self):
        super().__post_init__()
        assert self.dataset_name == 'employment_bus', "This class is specifically designed for the SPOLISBUS data table. Dataset name must be 'employment_bus'"

        # 88888888: start before reporting year
        # 99999999: no payments in reporting year
        if self.SDATUMAANVANGIKO == "88888888" or self.SDATUMAANVANGIKO == "99999999":
            self.month, self.day = None, None # TODO What do those code mean? Can we not find a year value for those? 
        # set year, month, and day values of parent class from employment start date of given reporting period
        else:
            pass
            # month = self.SDATUMAANVANGIKO[2:4]
            # day = self.SDATUMAANVANGIKO[:2]

            # # Convert them to integers (if needed)
            # self.month = int(month)
            # self.day = int(day)

