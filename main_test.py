from serialization.BookofLifeGenerator import BookofLifeGenerator

# Example usage:
generator = BookofLifeGenerator("00a2cd32", 'recipes/template.yaml')
print("Partner:", generator.social_context_paragraphs)
# print("Partner's child:", generator.social_context_paragraphs['household_bus']['partners'].social_context_paragraphs['household_bus']['children'].generate_book())
print('Main book:', generator.generate_book())
# print("Partner's child:", generator.social_context_paragraphs)

# print(generator.paragraphs[0].__annotations__)
### TODO write main for loop to geenrate and store BoLs here