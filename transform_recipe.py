import scraper
import ingredients
import foodsdb
import random
import json
from textblob import TextBlob
from nltk.tokenize import word_tokenize


class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()
        self.idb = foodsdb.RecipeDB('AllFoods.json')
        # self.russian = RussianFoods

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

        print(categories_dict)
        return categories_dict


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

        return info['ingredients']


    def get_np(self, text):
        tb = TextBlob(text)
        return tb.noun_phrases



    def transform_to_russian(self, rec):

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
        

        print(prep_list)
        categorized = self.get_categories(prep_list)

        with open("RussianFoods.json") as rf:
            russian_foods = json.load(rf)

        replacements = []

        for cat in categorized:
            randoms = []
            for ing in categorized[cat]:
                counter = 0
                for food in russian_foods[cat]:
                    if food in ing:
                        counter+=1
                if counter == 0:

                    random_replacement = random.choice(russian_foods[cat])
                    replacements.append([ing, random_replacement])
        
        print(replacements)
        for rep in replacements:
            for i in range(len(orig_ingredients)-1):
                
                if rep[0] in orig_ingredients[i]:
                    orig_ingredients[i] = (orig_ingredients[i].replace(rep[0], rep[1]))

        for rep in replacements:
            for i in range(len(orig_directions)-1):
                
                if rep[0] in orig_directions[i]:
                    orig_directions[i] = (orig_directions[i].replace(rep[0], rep[1]))

        
        return [orig_ingredients, orig_directions]


        




rt = RecipeTransformer()
food_item = "meat lasagna"


parsed = rt.transform_to_russian("meat lasagna")
print(parsed)
#original = rt.original_recipe(food_item)

'''
print('ORIGINAL')
for ingredient in original['ingredients']:
    print(ingredient)
for direction in original['directions']:
    print(direction)

print('primary methods:')
for primary_method in original['primary_methods']:
    print(primary_method)
print('secondary methods:')
for secondary_method in original['secondary_methods']:
    print(secondary_method)
'''

# healthy = rt.transform_health(food_item, False)
# print('\nHEALTHY')
# for ingredient in healthy[0]:
#     print(ingredient)
# for direction in healthy[1]:
#     print(direction)


# original = rt.original_recipe('meat lasagna')
# print('MEAT')
# for o in original:
#     print(o)

# vegetarian = rt.transform_to_vegetarian('meat lasagna')
# print('VEGETARIAN')
# for v in vegetarian:
#     print(v)

# c = rt.transform_method('meat lasagna', 'bake', 'fry')
# print('BAKE TO FRY')
# for ll in c:
#     print(ll)
