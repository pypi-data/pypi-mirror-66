from recipebook.constants import HEADER_CHAR, FOOTER_CHAR, HEADING

TOC_TEMPLATE: str = f"""
{HEADER_CHAR * 10}
Table of Contents
{HEADING * 10}
%s
{FOOTER_CHAR * 10}
 """


class TableOfContents:
    def __init__(self, cookbook):
        self.cookbook = cookbook

    def pretty_print(self) -> str:
        headlines = self.get_recipe_headlines()
        return TOC_TEMPLATE % headlines

    def get_recipe_headlines(self) -> str:
        if self.cookbook.recipes:
            return '\n'.join([f"{recipe.name} -> Time ({recipe.time})" for recipe in self.cookbook.recipes])

        return "You don't have any recipes at this time."
