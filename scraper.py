from bs4 import BeautifulSoup

import requests

import re


class RecipeFetcher:

    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'

    def search_recipes(self, keywords): 
        search_url = self.search_base_url %(keywords.replace(' ','+'))

        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content, features="html.parser")

        return [recipe.a['href'] for recipe in\
               page_graph.find_all('div', {'class':'grid-card-image-container'})]

    def scrape_recipe(self, recipe_url):
        results = {}

        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="html.parser")

        results['ingredients'] = [ingredient.text for ingredient in\
                                  page_graph.find_all('span', {'itemprop':'recipeIngredient'})]

        results['directions'] = [direction.text.strip() for direction in\
                                 page_graph.find_all('span', {'class':'recipe-directions__list--item'})
                                 if direction.text.strip()]

        #results['nutrition'] = self.scrape_nutrition_facts(recipe_url)

        return results
    '''
    def scrape_nutrition_facts(self, recipe_url):
        results = []

        nutrition_facts_url = '%s/fullrecipenutrition' %(recipe_url)

        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content)

        r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")

        for nutrient_row in <ITERATE_OVER_EACH_NUTRIENT>:
            nutrient = {}

            # Fill out this to scrape and return:
            # nutrient['name'], nutrient['amount'],
            # nutrient['unit'], nutrient['daily_value']
            
            results.append(nutrient)

        return results
    '''

# USAGE:
rf = RecipeFetcher()
meat_lasagna = rf.search_recipes('meat lasagna')[0]
info = rf.scrape_recipe(meat_lasagna)
print(info)

# for ingredient in info['ingredients']:
#     print(ingredient)
#
# for direct in info['directions']:
#     print(direct)