import scraper
import ingredients
import measurements
import tools
import foodsdb
import random
import json
import utils
import sys

class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()
        self.idb = foodsdb.RecipeDB('AllFoods.json')

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

    def get_tools(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        tools_used = []

        for i in range(len(info['directions'])):
            for tool in tools.tools:
                if tool not in tools_used and tool in info['directions'][i]:
                    tools_used.append(tool)
        return tools_used

    def get_measurements(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        measurements_used = []

        for i in range(len(info['ingredients'])):
            for measurement in measurements.measurements:
                if measurement not in measurements_used and measurement in info['ingredients'][i]:
                    measurements_used.append(measurement)
        return measurements_used

    def original_recipe(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        return info

    def transform(self, arr, is_healthy):
        for i in range(len(arr)):
            # if applicable, replace base grain with healthier version
            if is_healthy and not any(hp in arr[i] for hp in ingredients.healthy_prefixes):
                for grain in ingredients.grains:
                    if grain in arr[i]:
                        # randomly select from list of healthy prefixes
                        healthy_prefix = random.choice(ingredients.healthy_prefixes)
                        # print('replacing with healthy version:', healthy_prefix + grain)
                        new_ingredient = arr[i].replace(grain, healthy_prefix + grain)
                        arr[i] = new_ingredient
            elif not is_healthy:
                for hp in ingredients.healthy_prefixes:
                    if hp in arr[i]:
                        unhealthy_prefix = random.choice(ingredients.unhealthy_prefixes)
                        new_ingredient = arr[i].replace(hp, unhealthy_prefix)
                        arr[i] = new_ingredient

            healthy_ingredients = ingredients.ingredients_health['healthy']
            unhealthy_ingredients = ingredients.ingredients_health['unhealthy']
            if not is_healthy:
                healthy_ingredients, unhealthy_ingredients = unhealthy_ingredients, healthy_ingredients

            # replace unhealthy ingredients with a healthy ingredient of the corresponding type
            for unhealthy_ingredients_type in unhealthy_ingredients:
                for unhealthy_ingredient in unhealthy_ingredients_type:
                    if unhealthy_ingredient in arr[i]:
                        # print('\nunhealthy ingredient', unhealthy_ingredient, 'found in:', arr[i])
                        ind = unhealthy_ingredients.index(unhealthy_ingredients_type)
                        # randomly select from list of ingredients
                        healthy_ingredient = random.choice(healthy_ingredients[ind])
                        # print('replacing with healthy ingredient:', healthy_ingredient)
                        # self.mappings[unhealthy_ingredient] = healthy_ingredient
                        new_ingredient = arr[i].replace(unhealthy_ingredient, healthy_ingredient)
                        # change the ingredient in the list in the info dict
                        # print('adding to recipe:', new_ingredient)
                        arr[i] = new_ingredient
                        break
        return arr

    def transform_health(self, item, is_healthy):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        transformed_ingredients = self.transform(info['ingredients'], is_healthy)
        transformed_directions = self.transform(info['directions'], is_healthy)

        self.recipe_fetcher.results['ingredients'] = transformed_ingredients
        self.recipe_fetcher.results['directions'] = transformed_directions
        return transformed_ingredients, transformed_directions


    # alternate function using foods.json
    def transform_to_healthy2(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        food_json = json.loads(open('foods.json').read())

        for i in range(len(info['ingredients'])):
            for ingredient_alt in food_json['healthyToUnhealthy']:
                if ingredient_alt['unhealthy'] in info['ingredients'][i]:
                    new_ingredient = info['ingredients'][i].replace(ingredient_alt['unhealthy'], ingredient_alt['healthy'])
                    print('new healthy ingredient recipe:', new_ingredient)
                    info['ingredients'][i] = new_ingredient
                    break

        for i in range(len(info['directions'])):
            for ingredient_alt in food_json['healthyToUnhealthy']:
                if ingredient_alt['unhealthy'] in info['directions'][i]:
                    new_ingredient = info['directions'][i].replace(ingredient_alt['unhealthy'], ingredient_alt['healthy'])
                    print('new healthy ingredient recipe:', new_ingredient)
                    info['directions'][i] = new_ingredient
                    break
        self.recipe_fetcher.results = info
        return info

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
        self.recipe_fetcher.results = info
        return info['ingredients'], info['directions']

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
        self.recipe_fetcher.results = info
        return info['ingredients']

    def transform_method(self, item, method1, method2):
        #from method1 to method2
        #supports bake, boil, broil, fry, grill, steam, pressure cook, stir-fry, stew, and roast
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        methods = self.idb.m2t
        tools = self.idb.t2m
        if method1 not in methods:
            print('method1 not supported')
            return info['ingredients']
        if method2 not in methods:
            print('method2 not supported')
            return info['ingredients']

        for i in range(len(info['ingredients'])):
            entry = info['ingredients'][i].split(' ')
            new_entry = entry
            for element in entry:
                if element == method1:
                    new_entry = [method2 if wd == element else wd for wd in new_entry]
                if element == methods[method1]:
                    new_entry = [methods[method2] if wd == methods[method1] else wd for wd in new_entry]
                info['ingredients'][i] = " ".join(new_entry)
        
        for j in range(len(info['directions'])):
            direction = info['directions'][j].split(' ')
            direction = [direction.lower() for direction in direction]
            new_direction = direction
            for element in direction:
                if element == method1:
                    print(direction)
                    new_direction = [method2 if wd == element else wd for wd in new_direction]
                    print(new_direction)
                if element == methods[method1]:
                    new_direction = [methods[method2] if wd == methods[method1] else wd for wd in new_direction]
                info['directions'][j] = " ".join(new_direction)
        self.recipe_fetcher.results = info
        return info['ingredients'], info['directions']

    def transform_to_russian(self, item):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)

        self.get_categories(item)

    # amt is the amount to modify quantity by (double = 2, half = 0.5, etc.)
    def modify_quantity(self, item, amt):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        modified_ingredients = []

        for ing in info['ingredients']:
            modified_ingredients.append(utils.scale_fractional_quantity(ing, amt))

        return modified_ingredients

    def double_quantity(self, item, amt=2):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        modified_ingredients = []

        for ing in info['ingredients']:
            modified_ingredients.append(utils.scale_fractional_quantity(ing, amt))

        return modified_ingredients

    def halve_quantity(self, item, amt=0.5):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        modified_ingredients = []

        for ing in info['ingredients']:
            modified_ingredients.append(utils.scale_fractional_quantity(ing, amt))

        return modified_ingredients

def print_items(lst):
    print('\n')
    for item in lst:
        print(item)

def print_items2(dct):
    for d in dct:
        print_items(d)

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    rt = RecipeTransformer()
    while True:
        recipe = input("Recipe Name: ")
        print(
            "Options:\n"
            "1. Get Ingredients\n"
            "2. Get Awards\n"
            "3. Get Nominees\n"
            "4. Get Winners\n"
            "5. Get Presenters\n"
            "6. Get All\n"
            "7. Red Carpet Superlatives\n"
            "x. Exit Program")
        entry = input("Enter option: ")
        if entry == '1':
            print_items(rt.original_recipe(recipe)['ingredients'])
        elif entry == '2':
            print_items(rt.original_recipe(recipe)['directions'])
        elif entry == '3':
            print_items2(rt.transform_health(recipe, True))
        elif entry == '4':
            print_items2(rt.transform_health(recipe, False))
        elif entry == '5':
            print_items2(rt.transform_to_vegetarian(recipe))
        elif entry == '6':
            print_items2(rt.transform_to_carnivore(recipe))
        elif entry == '7':
            print_items2(rt.transform_to_carnivore(recipe))
        elif entry == '8':
            method1 = input("Enter cooking method 1"
                            " (bake, boil, broil, fry, grill, steam, pressure cook, stir-fry, stew, roast): ")
            method2 = input("Enter cooking method 2"
                            " (bake, boil, broil, fry, grill, steam, pressure cook, stir-fry, stew, roast): ")
            print_items2(rt.transform_method(recipe, method1, method2))
        elif entry == "x":
            sys.exit()
        else:
            print("Invalid input")


if __name__ == '__main__':
    main()
