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

            # self.seafood = json_data["seafood"]
            # self.dessert = json_data["dessert"]
            # self.veggie = json_data["veggie"]
            # self.other = json_data["veggie"]

            # self.hardFoodPrep = json_data["preparation"]["hardFoodPrep"]
            # self.regularFoodPrep = json_data["preparation"]["regularFoodPrep"]

            # set of seasons
            
            # set of styles
            # self.styles = json_data["styles"]

            # # set of measurements
            # self.solidMeasurements = json_data["measurement"]["solids"]
            # self.liquidMeasurements = json_data["measurement"]["liquids"]

            # # set of cooking methods
            # self.primaryMethods = json_data["methods"]["primary"]
            # self.secondaryMethods = json_data["methods"]["secondary"]

            # parse and get the healthy to unhealthy transformations
            # get the structure
            # healthyAndUnhealthy = json_data["healthyToUnhealthy"]
            # self.healthyToUnhealthy = {
            #     pairs["healthy"]: pairs["unhealthy"]
            #     for pairs in healthyAndUnhealthy
            # }
            # self.unhealthyToHealthy = {
            #     pairs["unhealthy"]: pairs["healthy"]
            #     for pairs in healthyAndUnhealthy
            # }
