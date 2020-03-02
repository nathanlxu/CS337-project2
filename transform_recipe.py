import scraper
import ingredients
import random
import json

class RecipeTransformer:
    def __init__(self):
        self.recipe_fetcher = scraper.RecipeFetcher()
        # self.mappings = {}

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


rt = RecipeTransformer()
food_item = "meat lasagna"

original = rt.original_recipe(food_item)
print('ORIGINAL')
for ingredient in original['ingredients']:
    print(ingredient)
for direction in original['directions']:
    print(direction)

healthy = rt.transform_health(food_item, False)
print('\nHEALTHY')
for ingredient in healthy[0]:
    print(ingredient)
for direction in healthy[1]:
    print(direction)