import pandas as pd
from serialization

def get_person_attributes(person_id: int, file_path: str) -> PersonAttributesParagraph:
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Find the row with the given person_id
    person_row = df[df['person_id'] == person_id].iloc[0]
    
    # Create the PersonAttributesParagraph object
    person_attributes = PersonAttributesParagraph(
        GBAGEBOORTELAND=person_row['GBAGEBOORTELAND'],
        GBAGESLACHT=person_row['GBAGESLACHT'],
        GBAGEBOORTEJAAR=person_row['GBAGEBOORTEJAAR'],
        GBAGEBOORTEMAAND=person_row['GBAGEBOORTEMAAND'],
        GBAGEBOORTEDAG=person_row['GBAGEBOORTEDAG'],
        GBAHERKOMSTLAND=person_row['GBAHERKOMSTLAND'],
        GBAGEBOORTELANDNL=person_row['GBAGEBOORTELANDNL'],
        GBAHERKOMSTGROEPERING=person_row['GBAHERKOMSTGROEPERING'],
        GBAGENERATIE=person_row['GBAGENERATIE'],
        GBAAANTALOUDERSBUITENLAND=person_row['GBAAANTALOUDERSBUITENLAND'],
        GBAGEBOORTELANDMOEDER=person_row['GBAGEBOORTELANDMOEDER'],
        GBAGESLACHTMOEDER=person_row['GBAGESLACHTMOEDER'],
        GBAGEBOORTEJAARMOEDER=person_row['GBAGEBOORTEJAARMOEDER'],
        GBAGEBOORTEMAANDMOEDER=person_row['GBAGEBOORTEMAANDMOEDER'],
        GBAGEBOORTEDAGMOEDER=person_row['GBAGEBOORTEDAGMOEDER'],
        GBAGEBOORTELANDVADER=person_row['GBAGEBOORTELANDVADER'],
        GBAGESLACHTVADER=person_row['GBAGESLACHTVADER'],
        GBAGEBOORTEJAARVADER=person_row['GBAGEBOORTEJAARVADER'],
        GBAGEBOORTEMAANDVADER=person_row['GBAGEBOORTEMAANDVADER'],
        GBAGEBOORTEDAGVADER=person_row['GBAGEBOORTEDAGVADER']
    )
    
    return person_attributes

# Example usage
file_path = 'synth/data/persoontab.csv'
person_id = 12345  # Replace with the actual person_id you want to query
person_attributes = get_person_attributes(person_id, file_path)
print(person_attributes)