import scraper
import ingredients
import foodsdb
import random

import json

class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()
        self.idb = foodsdb.RecipeDB('AllFoods.json')
        # self.russian = RussianFoods

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

        vegprot = self.idb.vegprot
        carnivore = self.idb.meat
        meat_desc = self.idb.descriptions['meat']
        m2v = self.idb.m2v
        for i in range(len(info['ingredients'])):
            entry = info['ingredients'][i].split(' ')
            new_entry = entry
            for element in entry:
                if element in carnivore:
                    removal = []
                    for descriptor in new_entry:
                        if descriptor in meat_desc:
                            removal.append(descriptor)
                    if element in m2v:
                        replacement = m2v[element]
                    else:
                        replacement = "potato" #default replacement
                    new_entry = [replacement if wd == element else wd for wd in new_entry]
                    for j in range(len(info['directions'])):
                        info['directions'][j] = info['directions'][j].replace(element, replacement)
                        info['directions'][j] = info['directions'][j].replace('meat', 'vegetarian alternative')
                    for rm in removal:
                        new_entry.remove(rm)
                    info['ingredients'][i] = " ".join(new_entry)
        print(info['directions'])
        return info['ingredients']

    def transform_to_carnivore(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        vegprot = self.idb.vegprot
        carnivore = self.idb.meat
        v2m = self.idb.v2m

        for i in range(len(info['ingredients'])):
            entry = info['ingredients'][i].split(' ')
            new_entry = entry
            for element in entry:
                if element in vegprot:
                    if element in v2m:
                        replacement = v2m[element]
                    else:
                        replacement = "chicken" #if no preset veg to meat alternative, go with chicken
                    for j in range(len(info['directions'])):
                        info['directions'][j] = info['directions'][j].replace(element, replacement)
                    new_entry = [replacement if wd == element else wd for wd in new_entry]
                    info['ingredients'][i] = " ".join(new_entry)
        return info['ingredients']

    def transform_to_russian(self, item):


        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        self.get_categories(item)



rt = RecipeTransformer()

original = rt.original_recipe('meat lasagna')

# rt.get_categories('meat lasagna')

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
    print(o)

vegetarian = rt.transform_to_vegetarian('meat lasagna')
print('VEGETARIAN')
for v in vegetarian:
    print(v)

c = rt.transform_to_carnivore('meat lasagna')
print('TO MEAT')
for ll in c:
    print(ll)
