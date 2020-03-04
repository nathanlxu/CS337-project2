from bs4 import BeautifulSoup

import requests

import re

import foodsdb


class RecipeFetcher:
	search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
	def search_recipes(self, keywords): 
		search_url = self.search_base_url %(keywords.replace(' ','+'))
		page_html = requests.get(search_url)
		page_graph = BeautifulSoup(page_html.content, features="html.parser")
		return [recipe.a['href'] for recipe in page_graph.find_all('div', {'class':'grid-card-image-container'})]
	def scrape_recipe(self, recipe_url):
		idb = foodsdb.RecipeDB('AllFoods.json')
		results = {}
		page_html = requests.get(recipe_url)
		page_graph = BeautifulSoup(page_html.content, features="html.parser")
		results['ingredients'] = [ingredient.text for ingredient in page_graph.find_all('span', {'itemprop':'recipeIngredient'})]
		results['directions'] = [direction.text.strip() for direction in page_graph.find_all('span', {'class':'recipe-directions__list--item'}) if direction.text.strip()]
		results['primary_methods'] = []
		results['secondary_methods'] = []
		for j in range(len(results['directions'])):
			direction = results['directions'][j].split(' ')
			for element in direction:
				if element in idb.pcm and element not in results['primary_methods']:
					results['primary_methods'].append(element)
				if element in idb.scm and element not in results['secondary_methods']:
					results['secondary_methods'].append(element)
		return results

rf = RecipeFetcher()
meat_lasagna = rf.search_recipes('cheese pizza')[0]
info = rf.scrape_recipe(meat_lasagna)
print(info)

# for ingredient in info['ingredients']:
#     print(ingredient)
#
# for direct in info['directions']:
#     print(direct)