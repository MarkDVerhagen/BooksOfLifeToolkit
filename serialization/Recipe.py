import yaml
from typing import List, Dict, Any, Union

class Recipe:
    def __init__(self, source: Union[str, Dict[str, Any]]):
        if isinstance(source, str):
            self.recipe_yaml_path = source
            self.recipe = self.load_recipe()
        elif isinstance(source, dict):
            self.recipe_yaml_path = None
            self.recipe = source
        else:
            raise ValueError("Source must be either a file path (str) or social_context_features (dict)")


    def load_recipe(self) -> Dict[str, Any]:
        with open(self.recipe_yaml_path, 'r') as file:
            recipe = yaml.load(file, Loader=yaml.FullLoader)
        return recipe

    @property
    def main_key(self) -> str:
        return self.recipe.get('main_key')

    @property
    def dataset_names(self) -> List[str]:
        datasets = self.recipe.get('datasets', [])
        names = [dataset.get('name') for dataset in datasets]
        return names
    
    @property
    def datasets(self) -> List[Dict[str, Any]]:
        return self.recipe.get('datasets', [])
    
    @property
    def social_context_features(self) -> List[Dict[str, Any]]:
        result = []
        for dataset in self.datasets:
            item = {
                dataset.get('name', 'unnamed_dataset'): {},
            }
            if 'social_context_features' in dataset:
                for context, features in dataset['social_context_features'].items():
                    item[dataset.get('name', 'unnamed_dataset')][context] = []
                    for feature_set in features:
                        if feature_set.get('social_context_features', None):
                            item[dataset.get('name', 'unnamed_dataset')][context].append({
                                'name': feature_set['name'],
                                'features': feature_set['features'],
                                'social_context_features': feature_set.get('social_context_features', None)
                            })
                        else:
                            item[dataset.get('name', 'unnamed_dataset')][context].append({
                                'name': feature_set['name'],
                                'features': feature_set['features']
                            })
                result.append(item)
        return result

    @property
    def sorting_keys(self) -> Dict[str, Any]:
        return self.recipe.get('formatting', {}).get('sorting_keys', {})
    
    @property
    def paragraph_generator(self) -> str:
        return self.recipe.get('formatting', {}).get('paragraph_generator', '')
    
    @property
    def formatting(self) -> Dict[str, Any]:
        return self.recipe.get('formatting', {})

    def get_features(self, dataset_name: str) -> List[str]:
        for dataset in self.datasets:
            if dataset.get('name') == dataset_name:
                return dataset.get('features', [])
        return []
