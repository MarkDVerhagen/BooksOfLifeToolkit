import duckdb
import json
from typing import List
from serialization.instantiator_scripts.EmploymentEventParagraph import EmploymentEventParagraph

# def get_employment_events(rinpersoon: str, db_name: str = 'synthetic_data.duckdb', table_version: str = '') -> List[EmploymentEventParagraph]: ## 20/8
def get_employment_events(rinpersoon: str, conn, table_version: str = '') -> List[EmploymentEventParagraph]: ## 20/8
    # conn = duckdb.connect(db_name, read_only=True) ## 20/8

    # Get the column names from the table
    columns_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'employment_bus'"
    columns = [row[0] for row in conn.execute(columns_query).fetchall()]

    query = f"""
    SELECT {', '.join(columns)} FROM employment_bus
    WHERE rinpersoon = ?
    """
    results = conn.execute(query, [rinpersoon]).fetchall()

    # Create a list to hold EmploymentEventParagraph objects
    employment_paragraphs = []

    # Iterate over each row to create EmploymentEventParagraph objects
    for row in results:
        # Convert row to a dictionary
        row_dict = dict(zip(columns, row))

        employment_paragraph = EmploymentEventParagraph(
            dataset_name="employment_bus",
            year=int(row_dict.get('year')),
            rinpersoon=rinpersoon,
            SIMPUTATIE=row_dict.get('SIMPUTATIE'),
            SINDWAARNEMING=row_dict.get('SINDWAARNEMING'),
            SDATUMAANVANGIKO=row_dict.get('SDATUMAANVANGIKO'),
            SDATUMAANVANGIKV=row_dict.get('SDATUMAANVANGIKV'),
            SDATUMAANVANGIKVORG=row_dict.get('SDATUMAANVANGIKVORG'),
            SDATUMEINDEIKO=row_dict.get('SDATUMEINDEIKO'),
            SDATUMEINDEIKV=row_dict.get('SDATUMEINDEIKV'),
            SBAANDAGEN=row_dict.get('SBAANDAGEN'),
            SVOLTIJDDAGEN=row_dict.get('SVOLTIJDDAGEN'),
            SAANTSV=row_dict.get('SAANTSV'),
            SREGULIEREUREN=row_dict.get('SREGULIEREUREN'),
            SWEKARBDUURKLASSE=row_dict.get('SWEKARBDUURKLASSE'),
            SAANTCTRCTURENPWK=row_dict.get('SAANTCTRCTURENPWK'),
            SAANTVERLU=row_dict.get('SAANTVERLU'),
            SBASISUREN=row_dict.get('SBASISUREN'),
            SOVERWERKUREN=row_dict.get('SOVERWERKUREN'),
            SFSINDFZ=row_dict.get('SFSINDFZ'),
            STIJDVAKTYPE=row_dict.get('STIJDVAKTYPE'),
            SPOLISDIENSTVERBAND=row_dict.get('SPOLISDIENSTVERBAND'),
            SARBEIDSRELATIE=row_dict.get('SARBEIDSRELATIE'),
            SOVERWERK=row_dict.get('SOVERWERK'),
            INDPUBAANONBEPTD=row_dict.get('INDPUBAANONBEPTD'),
            SBEID=row_dict.get('SBEID'),
            SCAOSECTOR=row_dict.get('SCAOSECTOR'),
            SSECT=row_dict.get('SSECT'),
            SSOORTBAAN=row_dict.get('SSOORTBAAN'),
            SWGHZVW=row_dict.get('SWGHZVW'),
            PrAwfLg=row_dict.get('PrAwfLg'),
            PrAwfHg=row_dict.get('PrAwfHg'),
            PrAwfHz=row_dict.get('PrAwfHz'),
            SBASISLOON=row_dict.get('SBASISLOON'),
            SCTRCTLN=row_dict.get('SCTRCTLN'),
            SSRTIV=row_dict.get('SSRTIV'),
            SINCIDENTSAL=row_dict.get('SINCIDENTSAL'),
            SCDINCINKVERM=row_dict.get('SCDINCINKVERM'),
            SLNINGLD=row_dict.get('SLNINGLD'),
            SWRDLN=row_dict.get('SWRDLN'),
            PRLNUFO=row_dict.get('PRLNUFO'),
            PRLNAWFANWLg=row_dict.get('PRLNAWFANWLg'),
            PRLNAWFANWHg=row_dict.get('PRLNAWFANWHg'),
            PRLNAWFANWHz=row_dict.get('PRLNAWFANWHz'),
            PRLNAOFANWHG=row_dict.get('PRLNAOFANWHG'),
            PRLNAOFANWLG=row_dict.get('PRLNAOFANWLG'),
            PRLNAOFANWUIT=row_dict.get('PRLNAOFANWUIT'),
            SINDWAO=row_dict.get('SINDWAO'),
            SINDWW=row_dict.get('SINDWW'),
            SLNSV=row_dict.get('SLNSV'),
            SRISGRP=row_dict.get('SRISGRP'),
            SINGLBPH=row_dict.get('SINGLBPH'),
            SLNLBPH=row_dict.get('SLNLBPH'),
            SCDINVLVPL1=row_dict.get('SCDINVLVPL1'),
            SCDINVLVPL2=row_dict.get('SCDINVLVPL2'),
            SCDINVLVPL3=row_dict.get('SCDINVLVPL3'),
            SVERSTRAANV=row_dict.get('SVERSTRAANV'),
            SVERGZVW=row_dict.get('SVERGZVW'),
            SPENSIOENPREMIE=row_dict.get('SPENSIOENPREMIE'),
            SBEDRZDAFTR=row_dict.get('SBEDRZDAFTR'),
            SBIJDRZVW=row_dict.get('SBIJDRZVW'),
            SLBTAB=row_dict.get('SLBTAB'),
            SLHNR_crypt=row_dict.get('SLHNR_crypt'),
            SCDZVW=row_dict.get('SCDZVW'),
            SBEDRRCHTAL=row_dict.get('SBEDRRCHTAL'),
            SBEDRALINWWB=row_dict.get('SBEDRALINWWB'),
            SLNTABBB=row_dict.get('SLNTABBB'),
            SREISK=row_dict.get('SREISK'),
            SWGBIJDRKO=row_dict.get('SWGBIJDRKO'),
            OPSLWKO=row_dict.get('OPSLWKO'),
            OPBAVWB=row_dict.get('OPBAVWB'),
            OPNAVWB=row_dict.get('OPNAVWB'),
            PRAOFHG=row_dict.get('PRAOFHG'),
            PRAOFLG=row_dict.get('PRAOFLG'),
            PRAOFUIT=row_dict.get('PRAOFUIT'),
            SAUTOVANDEZAAK=row_dict.get('SAUTOVANDEZAAK'),
            SWRDPRGEBRAUT=row_dict.get('SWRDPRGEBRAUT'),
            SAUTOZAAK=row_dict.get('SAUTOZAAK'),
            SWRKNBIJDRAUT=row_dict.get('SWRKNBIJDRAUT'),
            SCDRDNGNBIJT=row_dict.get('SCDRDNGNBIJT'),
            SBIJZONDEREBELONING=row_dict.get('SBIJZONDEREBELONING'),
            SEXTRSAL=row_dict.get('average_salary_while_employed'),
            SLNOWRK=row_dict.get('SLNOWRK'),
            SLVLPREG=row_dict.get('SLVLPREG'),
            SLVLPREGTOEG=row_dict.get('SLVLPREGTOEG'),
            SVERRARBKRT=row_dict.get('SVERRARBKRT'),
            SINDTIJDHK=row_dict.get('SINDTIJDHK'),
            SOPGRCHTEXTRSAL=row_dict.get('SOPGRCHTEXTRSAL'),
            SVAKBSL=row_dict.get('SVAKBSL'),
            SOPGRCHTVAKBSL=row_dict.get('SOPGRCHTVAKBSL'),
            SBEDRRNTKSTVPERSL=row_dict.get('SBEDRRNTKSTVPERSL'),
            SModelramingPensioenpremieWn=row_dict.get('SModelramingPensioenpremieWn'),
            SModelramingPensioenpremieWg=row_dict.get('SModelramingPensioenpremieWg'),
            SModelramingVutpremieWn=row_dict.get('SModelramingVutpremieWn'),
            SModelramingVutpremieWg=row_dict.get('SModelramingVutpremieWg'),
            SModelramingSFpremieWg=row_dict.get('SModelramingSFpremieWg'),
            SINDSA03=row_dict.get('SINDSA03'),
            SINDLHKORT=row_dict.get('SINDLHKORT'),
            SINDSA43=row_dict.get('SINDSA43'),
            SINDSA71=row_dict.get('SINDSA71'),
            SINDSA72=row_dict.get('SINDSA72'),
            SINDVAKBN=row_dict.get('SINDVAKBN'),
            SINDZW=row_dict.get('SINDZW'),
            SINLEGLEVENSLOOP=row_dict.get('SINLEGLEVENSLOOP'),
            INDDEELNTIJDSPF=row_dict.get('INDDEELNTIJDSPF'),
            SINDPRKJONGRWEN=row_dict.get('SINDPRKJONGRWEN'),
            SINDPKNWARBVOUDWN=row_dict.get('SINDPKNWARBVOUDWN'),
            SINDPKAGH=row_dict.get('SINDPKAGH'),
            SINDPMA=row_dict.get('SINDPMA'),
            SIndAvrLkvOudrWn=row_dict.get('SIndAvrLkvOudrWn'),
            SIndAvrLkvAgWn=row_dict.get('SIndAvrLkvAgWn'),
            SIndAvrLkvDgBafSb=row_dict.get('SIndAvrLkvDgBafSb'),
            SIndAvrLkvHpAgWn=row_dict.get('SIndAvrLkvHpAgWn'),
            CdRdnEindArbov=row_dict.get('CdRdnEindArbov'),
            SPRAWF=row_dict.get('SPRAWF'),
            SPRUFO=row_dict.get('SPRUFO'),
            SPRWAOAOF=row_dict.get('SPRWAOAOF'),
            SPRWAOAOK=row_dict.get('SPRWAOAOK'),
            SPRWGAWHK=row_dict.get('SPRWGAWHK'),
            SPRGEDIFFWHK=row_dict.get('SPRGEDIFFWHK'),
            PRLNWHKANW=row_dict.get('PRLNWHKANW'),
            PRLNAWFANWUIT=row_dict.get('PRLNAWFANWUIT'),
            PRAWFUIT=row_dict.get('PRAWFUIT'),
            SCDAGH=row_dict.get('SCDAGH'),
            SPRWGF=row_dict.get('SPRWGF'),
            SCONTRACTSOORT=row_dict.get('SCONTRACTSOORT'),
            SCAO_crypt=row_dict.get('SCAO_crypt'),
            SCDAARD=row_dict.get('SCDAARD'),
            CdCaoInl_crypt=row_dict.get('CdCaoInl_crypt'),
            IndArbovOnbepTd=row_dict.get('IndArbovOnbepTd'),
            IndSchriftArbov=row_dict.get('IndSchriftArbov'),
            IndOprov=row_dict.get('IndOprov'),
            IndJrurennrm=row_dict.get('IndJrurennrm')
        )

        employment_paragraphs.append(employment_paragraph)

    # Close the database connection
    # conn.close() ## 20/8

    return employment_paragraphs

