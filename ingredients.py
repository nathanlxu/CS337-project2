# list of healthy and unhealthy ingredients
# source: https://github.com/olivergoodman/food-recipes/blob/master/transforms.py

healthy_fats = ['olive oil', 'sunflower oil', 'soybean oil', 'corn oil',  'sesame oil',  'peanut oil']
unhealthy_fats = ['butter', 'lard', 'shortening', 'canola oil', 'margarine', 'coconut oil', 'tallow', 'cream', 'milk fat', 'palm oil', 'palm kemel oil', 'chicken fat', 'hydrogenated oils']
healthy_protein = ['peas', 'beans', 'eggs', 'crab', 'fish','chicken', 'tofu', 'liver', 'turkey']
unhealthy_protein = ['ground beef', 'beef', 'pork', 'lamb']
healthy_dairy = ['fat free milk', 'low fat milk', 'yogurt', 'low fat cheese']
unhealthy_dairy = ['reduced-fat milk', 'cream cheese', 'whole milk', 'butter', 'whipped cream',  'sour cream']
healthy_grains = ['wild rice', 'oatmeal', 'whole rye', 'buckwheat', 'quinoa', 'bulgur', 'millet', 'brown rice', 'whole wheat pasta']
unhealthy_grains = ['macaroni', 'spaghetti', 'white rice', 'white bread', 'white pasta']
healthy_salts = ['low sodium soy sauce', 'sea salt', 'kosher salt']
unhealthy_salts = ['soy sauce', 'table salt', 'salt']
healthy_sugars = ['real fruit jam', 'fruit juice concentrates', 'monk fruit extract', 'cane sugar', 'molasses', 'brown rice syrup' 'stevia', 'honey', 'maple syrup', 'agave syrup', 'coconut sugar', 'date sugar', 'sugar alcohols', 'brown sugar']
unhealthy_sugars = ['aspartame', 'acesulfame K', 'sucralose', 'white sugar', 'corn syrup', 'chocolate syrup']
healthy_methods = ['boil']
unhealthy_methods = ['fry']
healthy_storage = ['fresh']
unhealthy_storage = ['frozen', 'refrigerated']

ingredients_health = {'healthy': [healthy_dairy, healthy_fats, healthy_methods,
                                  healthy_protein, healthy_salts, healthy_sugars, healthy_storage],
                      'unhealthy': [unhealthy_dairy, unhealthy_fats, unhealthy_methods,
                                    unhealthy_protein, unhealthy_salts, unhealthy_sugars, unhealthy_storage]}

healthy_prefixes = ['whole grain ', 'whole wheat ', 'whole rye ', 'buckwheat ']
unhealthy_prefixes = ['white ', 'enriched wheat ', 'refined wheat ', 'enriched rye ', 'processed ']
grains = ['rice', 'macaroni', 'spaghetti', 'noodle', 'pasta']