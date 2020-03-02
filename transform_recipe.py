import scraper
import ingredients
import random

class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()

    def original_recipe(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        # print("RECIPE:", info['ingredients'])
        return info['ingredients']

    def transform_to_healthy(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        healthy_ingredients = ingredients.ingredients_health['healthy']
        unhealthy_ingredients = ingredients.ingredients_health['unhealthy']

        for i in range(len(info['ingredients'])):
            # replace unhealthy ingredients with a healthy ingredient of the corresponding type
            for unhealthy_ingredients_type in unhealthy_ingredients:
                for unhealthy_ingredient in unhealthy_ingredients_type:
                    if unhealthy_ingredient in info['ingredients'][i]:
                        print('\nunhealthy ingredient', unhealthy_ingredient, 'found in:', info['ingredients'][i])
                        ind = unhealthy_ingredients.index(unhealthy_ingredients_type)
                        # randomly select from list of ingredients
                        healthy_ingredient = random.choice(healthy_ingredients[ind])
                        print('replacing with healthy ingredient:', healthy_ingredient)
                        new_ingredient = info['ingredients'][i].replace(unhealthy_ingredient, healthy_ingredient)
                        # change the ingredient in the list in the info dict
                        print('adding to recipe:', new_ingredient)
                        info['ingredients'][i] = new_ingredient
                        break

        return info['ingredients']


rt = RecipeTransformer()

original = rt.original_recipe('meat lasagna')
print('ORIGINAL')
for o in original:
    print(o)

healthy = rt.transform_to_healthy('meat lasagna')
print('\nHEALTHY')
for h in healthy:
    print(h)