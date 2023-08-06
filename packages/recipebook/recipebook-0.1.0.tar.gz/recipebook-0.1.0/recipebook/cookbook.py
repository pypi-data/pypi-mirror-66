from typing import List

from recipebook.recipe import Recipe
from recipebook.toc import TableOfContents


class Cookbook:
    def __init__(self):
        self.table_of_contents = TableOfContents(self)
        self.recipes: List[Recipe] = list()

