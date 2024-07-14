import yaml
from typing import List, Dict, Any

class Recipe:
    def __init__(self, recipe_yaml_path: str):
        self.recipe_yaml_path = recipe_yaml_path
        self.recipe = self.load_recipe()

    def load_recipe(self) -> Dict[str, Any]:
        with open(self.recipe_yaml_path, 'r') as file:
            recipe = yaml.load(file, Loader=yaml.FullLoader)
        return recipe

    @property
    def main_key(self) -> str:
        return self.recipe.get('main_key')

    @property
    def dataset_names(self) -> List[Dict[str, Any]]:
        datasets = self.recipe.get('datasets', [])
        names = [dataset.get('name') for dataset in datasets]
        return names
    
    @property
    def datasets(self) -> List[Dict[str, Any]]:
        return self.recipe.get('datasets', [])

    @property
    def sorting_keys(self) -> Dict[str, Any]:
        return self.recipe.get('formatting', {}).get('sorting_keys', {})
    
    @property
    def paragraph_generator(self) -> str:
        return self.recipe.get('formatting', {}).get('paragraph_generator', '')

    def get_excluded_features(self, dataset_name: str) -> List[str]:
        for dataset in self.datasets:
            if dataset.get('name') == dataset_name:
                return dataset.get('excluded_features', [])
        return []

# Example usage:
# recipe = Recipe('recipes/template.yaml')
# print(recipe.dataset_names)
# print(recipe.sorting_keys)
# print(recipe.paragraph_generator)
# print(recipe.get_excluded_features('householdbus'))
