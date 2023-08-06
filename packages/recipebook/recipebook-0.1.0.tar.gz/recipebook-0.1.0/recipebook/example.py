from recipebook.cookbook import Cookbook
from recipebook.recipe import Recipe, Time


def main():
    cookbook = Cookbook()
    print(cookbook.table_of_contents.pretty_print())

    print('Adding two recipes.')
    cookbook.recipes.append(Recipe("Chickpea Burgers", Time(40, Time.Unit.MINUTES)))
    cookbook.recipes.append(Recipe("Black Bean Burgers", Time(45, Time.Unit.MINUTES)))
    cookbook.recipes.append(Recipe("Homemade Sesame Seed Hamburger Buns", Time(2, Time.Unit.HOURS)))

    print(cookbook.table_of_contents.pretty_print())


if __name__ == '__main__':
    main()

