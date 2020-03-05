import scraper
import ingredients
import measurements
import tools
import foodsdb
import random
import json
import utils
import sys
from textblob import TextBlob
from nltk.tokenize import word_tokenize


class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()
        self.idb = foodsdb.RecipeDB('AllFoods.json')

    def get_categories(self, ingredients):
        with open("AllFoods.json") as foods:
            all_foods = json.load(foods)
        categories = ["AllVeg", "AllCarbs", "AllProteins", "AllSpices", "AllFats", "AllCondiments"]
        categories_dict = {
            "AllCarbs": [],
            "AllProteins": [],
            "AllVeg": [],
            "AllSpices": [],
            "AllFats": [],
            "AllCondiments": []
        }
        for ingredient in ingredients:
            for cat in categories:
                for food in all_foods[cat]:
                    if food in ingredient:
                #if ingredient in all_foods[cat]:
                        categories_dict[cat].append(ingredient)
        for cat_list in categories_dict:
            categories_dict[cat_list] = list(set(categories_dict[cat_list]))

        for food in categories_dict["AllProteins"]:
            if food in categories_dict["AllCarbs"]:
                categories_dict["AllCarbs"].remove(food)

        for food in categories_dict["AllVeg"]:
            if food in categories_dict["AllSpices"]:
                categories_dict["AllSpices"].remove(food)

        for food in categories_dict["AllCondiments"]:
            if food in categories_dict["AllVeg"]:
                categories_dict["AllVeg"].remove(food)

        for food in categories_dict["AllCondiments"]:
            if food in categories_dict["AllCarbs"]:
                categories_dict["AllCarbs"].remove(food)

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


    def get_np(self, text):
        tb = TextBlob(text)
        return tb.noun_phrases


    def transform_to_cuisine(self, rec, cuisine):

        measurements = ["ounce", "ounces", "cup", "cups", "quart", "quarts", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "pinch", "dash", "gallon", "gallons", 'package', "packages",
"oz", "qt", "tsp", "tbsp", "gal", "pound", "lb", "pounds", "lbs", "jars", "jar", "or", "to", "taste", ",", "for"]

        original = self.original_recipe(rec)
        orig_ingredients = original["ingredients"]
        orig_directions = original["directions"]

        for i in range(len(orig_ingredients) - 1):
            orig_ingredients[i] = orig_ingredients[i].lower()

        for j in range(len(orig_directions) - 1):
            orig_directions[j] = orig_directions[j].lower()

        prep_list = []
        for ing in orig_ingredients:
            #tb = TextBlob(ing)
            tokenized = word_tokenize(ing)
            for word in tokenized:
                if word.isnumeric():
                    tokenized.remove(word)
                if word in measurements:
                    tokenized.remove(word)

            untokenized = ' '.join(tokenized)
            untokenized_tb = TextBlob(untokenized)
            np = untokenized_tb.noun_phrases
            if len(np) == 0:
                np = untokenized
            else:
                np = np[0]

            prep_list.append(np)


        categorized = self.get_categories(prep_list)

        with open(cuisine+"Foods.json") as rf:
            cuisine_foods = json.load(rf)

        replacements = []

        for cat in categorized:
            randoms = []
            for ing in categorized[cat]:
                counter = 0
                for food in cuisine_foods[cat]:
                    if food in ing:
                        counter+=1
                if counter == 0:

                    random_replacement = random.choice(cuisine_foods[cat])
                    replacements.append([ing, random_replacement])

        for rep in replacements:
            for i in range(len(orig_ingredients)-1):

                if rep[0] in orig_ingredients[i]:
                    orig_ingredients[i] = (orig_ingredients[i].replace(rep[0], rep[1]))

        for rep in replacements:
            for i in range(len(orig_directions)-1):

                if rep[0] in orig_directions[i]:
                    orig_directions[i] = (orig_directions[i].replace(rep[0], rep[1]))

        final_list = [orig_ingredients, orig_directions]
        return final_list

    # amt is the amount to modify quantity by (double = 2, half = 0.5, etc.)
    def modify_quantity(self, item, amt):
        rf = self.recipe_fetcher
        recipe = rf.search_recipes(item)[0]
        info = rf.scrape_recipe(recipe)
        modified_ingredients = []
        modified_directions = []

        for ing in info['ingredients']:
            modified_ingredients.append(utils.scale_fractional_quantity(ing, amt))
        for ing in info['directions']:
            modified_directions.append(utils.scale_fractional_quantity(ing, amt))

        return modified_ingredients, modified_directions

    def double_quantity(self, item, amt=2):
        return self.modify_quantity(item, amt)

    def halve_quantity(self, item, amt=0.5):
        return self.modify_quantity(item, amt)


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
    item = input("Enter a recipe name: ")
    while True:
        recipe = input("\nPress <ENTER> to CONTINUE with this recipe, or type a new recipe name to CHANGE: ")
        if not recipe:
            recipe = item
        print(
            "Enter one of the following:\n"
            "ingredients\n"
            "directions\n"
            "tools\n"
            "measurements\n"
            "primary cooking method\n"
            "to healthy\n"
            "to unhealthy\n"
            "to vegetarian\n"
            "to carnivore\n"
            "to russian\n"
            "to italian\n"
            "double quantity\n"
            "halve quantity\n"
            "enter 'x' to exit program")
        entry = input("\nEnter option: ")
        if entry == 'ingredients':
            print_items(rt.original_recipe(recipe)['ingredients'])
        elif entry == 'directions':
            print_items(rt.original_recipe(recipe)['directions'])
        elif entry == 'tools':
            print_items(rt.get_tools(recipe))
        elif entry == 'measurements':
            print_items(rt.get_measurements(recipe))
        elif entry == 'primary cooking method':
            rec = rt.recipe_fetcher.search_recipes(recipe)[0]
            info = rt.recipe_fetcher.scrape_recipe(rec)
            for method in info["primary_methods"]:
                print(method)
            #print(info["primary_methods"])
        elif entry == 'to healthy':
            print_items2(rt.transform_health(recipe, True))
        elif entry == 'to unhealthy':
            print_items2(rt.transform_health(recipe, False))
        elif entry == 'to vegetarian':
            print_items2(rt.transform_to_vegetarian(recipe))
        elif entry == 'to carnivore':
            print_items2(rt.transform_to_carnivore(recipe))
        elif entry == 'to russian':
            print_items2(rt.transform_to_cuisine(recipe, 'Russian'))
        elif entry == 'to italian':
            print_items2(rt.transform_to_cuisine(recipe, 'Italian'))
        elif entry == 'double quantity':
            print_items2(rt.double_quantity(recipe))
        elif entry == 'halve quantity':
            print_items2(rt.halve_quantity(recipe))
        elif entry == 'change cooking method':
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
