import scraper
import ingredients
import foodsdb
import random

import json

class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()
        self.ingredients = foodsdb.RecipeDB('AllFoods.json')
        self.all = AllFoods
        self.russian = RussianFoods

    def get_categories(self, item):
        with open("AllFoods.json") as foods:
            all_foods = json.loads(foods)
        categories = ["Veg", "Carbs", "Proteins", "Spices", "Fats", "Condiments"]
        categories_dict = {
            "Carbs": [],
            "Proteins": [],
            "Veg": [],
            "Spices": [],
            "Fats": [],
            "Condiments": []
        }
        recipe = self.original_recipe(item)
        for ingredient in recipe:
            for cat in categories:
                if ingredient in all_foods[cat]:
                     categories_dict[cat].append(ingredient)
        print(categories_dict)
        return categories_dict
        


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

    def transform_to_vegetarian(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        vegetarian = self.ingredients.veggie
        carnivore = self.ingredients.meat
        print(info['ingredients'])

        for lst in info['ingredients']:
            for ingredient in lst.split(' '):
                if ingredient in self.ingredients.all_ingredients:
                    print(ingredient)
                if ingredient in self.ingredients.meat:
                    print('this is meat^')
        return info['ingredients']

    def transform_to_russian(self, item):


        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        self.get_categories(item)




rt = RecipeTransformer()

original = rt.original_recipe('meat lasagna')

rt.get_categories('meat lasagna')

print('ORIGINAL')
for o in original:
    print(o)

healthy = rt.transform_to_healthy('meat lasagna')
print('\nHEALTHY')
for h in healthy:
    print(h)

original = rt.original_recipe('meat lasagna')
print('MEAT')
for o in original:
    d = 0

vegetarian = rt.transform_to_vegetarian('meat lasagna')
print('VEGETARIAN')
for v in vegetarian:
    d = 0
    # print(v)
