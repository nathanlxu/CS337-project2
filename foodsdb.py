import json
import random


class RecipeDB:
    def __init__(self, path):
        # open the file
        with open(path) as f:
            json_data = json.load(f)
            # self.tools = json_data["tools"]
            
            self.veggie = json_data["AllVeg"]
            self.spice = [spice.lower() for spice in json_data["AllSpices"]]
            self.condiments = [condiment.lower() for condiment in json_data["AllCondiments"]]
            self.carbs = json_data["AllCarbs"]
            self.fats = json_data["AllFats"]
            self.proteins = json_data["AllProteins"]
            self.meat = json_data["MeatProtein"]
            self.vegprot = json_data["VegetarianProtein"]
            self.all_ingredients = self.veggie + self.spice + self.condiments + self.carbs + self.fats + self.proteins
            self.descriptions = json_data['descriptions']
            self.alternates = json_data['alternates']
            self.m2v = {}
            self.v2m = {}
            for alternate in self.alternates:
                self.m2v[alternate[0]] = alternate[1]
                self.v2m[alternate[1]] = alternate[0]

            self.methods = json_data['methods']
            self.m2t = {}
            self.t2m = {}
            for method in self.methods:
                self.m2t[method[0]] = method[1]
                self.t2m[method[1]] = method[0]
            self.pcm = json_data['cooking_methods']['primary']
            self.scm = json_data['cooking_methods']['secondary']