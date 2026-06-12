from operator import attrgetter
import duckdb

from serialization.Recipe import Recipe
from serialization.registry import get_instantiator

class BookofLifeGenerator:
    def __init__(
        self,
        rinpersoon,
        recipe_yaml_path,
        paragraphs=None,
        duck_db_conn=None,
        table_version: str = "",
        social_depth: int = 3,
    ):
        """Create a Book-of-Life generator.

        Parameters
        ----------
        rinpersoon : str
            Unique identifier of the individual.
        recipe_yaml_path : str or Path
            Path to the recipe YAML that drives the narrative.
        paragraphs : list[Paragraph] | None, default None
            If provided, these Paragraph objects will be used directly. If
            *None*, the class will instantiate them by querying *duck_db_conn*.
        duck_db_conn : duckdb.DuckDBPyConnection | None, default None
            Connection to a DuckDB database that contains all required tables.
            Required to instantiate paragraphs from the database *and* to write
            "books within books" for social-context members.
        table_version : str, default ""
            Optional suffix appended to table names (e.g., "_v1").
        social_depth : int, default 3
            Maximum recursion depth for nested "books within books". Guards
            against the infinite regress that arises with self-referential
            recipes (e.g. a household that includes partners whose books again
            include their household). Set to 0 to disable nested books.
        """

        self.rinpersoon = rinpersoon
        self.recipe = Recipe(recipe_yaml_path)
        self.book: str = ""
        self.table_version = table_version
        self.social_depth = social_depth

        # Detect legacy positional usage where a DuckDB connection was provided
        # as the third positional arg (previously `duck_db_conn`).
        if paragraphs is not None and isinstance(paragraphs, duckdb.DuckDBPyConnection) and duck_db_conn is None:
            duck_db_conn = paragraphs
            paragraphs = None

        # Save connection (may be None if paragraphs were supplied)
        self.conn = duck_db_conn

        if paragraphs is not None:
            # Use the supplied paragraphs directly
            self.paragraphs = paragraphs
        else:
            if self.conn is not None:
                # Build paragraphs automatically from the database
                self.paragraphs = self.instantiate_paragraphs()
            else:
                # No connection and no supplied paragraphs – leave empty.
                self.paragraphs = []

    def instantiate_paragraphs(self):
        """Query the database and create Paragraph objects for *rinpersoon*."""

        paragraphs_list = []

        for dataset in self.recipe.datasets:
            dataset_name = dataset.get("name")
            explicit = dataset.get("explicit", False)
            order = dataset.get("sort_key", 0)

            instantiator = get_instantiator(dataset_name, self.table_version)
            par_dict = instantiator(
                [self.rinpersoon], self.conn, self.table_version, explicit, order
            )

            # Extend paragraph list with the paragraphs for this rinpersoon if available
            if self.rinpersoon in par_dict:
                paragraphs_list.extend(par_dict[self.rinpersoon])

        return paragraphs_list

    def sort_paragraphs(self):
        '''sort paragraphs based on sorting keys.'''
        
        ## Start by adding custom keys if present
        # getattr(paragraph, )
        
        sorting_keys = self.recipe.sorting_keys

        if isinstance(sorting_keys, str):
            sorting_keys = [sorting_keys]
        
        supported_sorting_keys = ['year', 'dataset_name', 'year_dataset_name',
                                  'year_month_day']

        # Assert that all elements in sorting_keys are either 'year' or 'dataset_name'
        assert all(key in supported_sorting_keys for key in sorting_keys), "sorting_keys contains values outside of 'year' and 'dataset_name'"

        sorting_keys = ['order'] + sorting_keys

        self.paragraphs.sort(key=attrgetter(*sorting_keys))

        new_pars = []
        for info in self.recipe.datasets:
            sub_pars = []
            name = info.get('name')
            n_spell = info.get('n_spell', None)
            sort_key = info.get('sort_key', None)
            min_spell_year = info.get('min_spell_year', None)
            max_spell_year = info.get('max_spell_year', None)
            sub_pars = [p for p in self.paragraphs if p.dataset_name == str(name)]
            
            if n_spell:
                # Keep the ``n_spell`` most recent paragraphs. Paragraphs are
                # already sorted chronologically, so the most recent ones are at
                # the end of the list.
                addition = sub_pars[-n_spell:]
            else:
                addition = sub_pars
            if not isinstance(addition, list):
                addition = [addition]
            
            if min_spell_year:
                if addition:
                    addition = [a for a in addition if a.spell_year_start >= min_spell_year or a.spell_year_end >= min_spell_year]
            if max_spell_year:
                if addition:
                    addition = [a for a in addition if a.spell_year_start <= max_spell_year or a.spell_year_end <= max_spell_year]
            new_pars.extend(addition)
            
        self.paragraphs = new_pars

        self.paragraphs.sort(key=attrgetter(*sorting_keys))

        return self.paragraphs

    def _context_by_dataset(self):
        """Map ``dataset_name`` -> ``{context_name: [nested dataset specs]}``.

        Built from the recipe's ``social_context_features``. Empty when the
        recipe requests no social context.
        """
        mapping = {}
        for item in self.recipe.social_context_features:
            for dataset_name, contexts in item.items():
                if contexts:
                    mapping[dataset_name] = contexts
        return mapping

    def _render_social_context(self, paragraph, contexts, generator_function):
        """Write nested books for the social-context members of *paragraph*."""
        section = ""
        for context_name, feature_sets in contexts.items():
            member_ids = getattr(paragraph, context_name, None) or []
            for member_id in member_ids:
                sub_recipe = {
                    "main_key": self.recipe.main_key,
                    "datasets": feature_sets,
                    "formatting": {
                        "sorting_keys": self.recipe.sorting_keys,
                        "paragraph_generator": generator_function,
                    },
                }
                sub_book = BookofLifeGenerator(
                    rinpersoon=member_id,
                    recipe_yaml_path=sub_recipe,
                    duck_db_conn=self.conn,
                    table_version=self.table_version,
                    social_depth=self.social_depth - 1,
                ).generate_book().strip()
                if sub_book:
                    indented = "\n".join("    " + line for line in sub_book.splitlines())
                    section += f"\n\n  [{context_name} {member_id}]\n{indented}"
        return section

    def write_book(self, generator_function):
        assert self.book == "", "Book is not empty"
        # Social context (books within books) needs a live connection to look up
        # members, and is bounded by ``social_depth`` to avoid infinite regress.
        context_by_dataset = (
            self._context_by_dataset()
            if self.conn is not None and self.social_depth > 0
            else {}
        )
        for paragraph in self.paragraphs:
            paragraph_string = getattr(paragraph, generator_function)(self.recipe.get_features(paragraph.dataset_name))
            self.book += "\n\n" + paragraph_string
            contexts = context_by_dataset.get(paragraph.dataset_name)
            if contexts:
                self.book += self._render_social_context(paragraph, contexts, generator_function)

    def generate_book(self):
        self.sort_paragraphs()
        self.write_book(self.recipe.paragraph_generator)

        if self.recipe.formatting.get('header', False):
            self.book += f"\n\nThis was the Book of Life of {self.rinpersoon}."

        return self.book

    