import nltk
import re
import pprint
from nltk import Tree
from transform_recipe import RecipeTransformer

patterns = """
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    """

NPChunker = nltk.RegexpParser(patterns)

def prepare_text(input):
    #sentences = nltk.sent_tokenize(input)
    sentences = nltk.word_tokenize(input)
    sentences = nltk.pos_tag(sentences)
    sentences = NPChunker.parse(sentences)
    return sentences


def parsed_text_to_NP(sentences):
    nps = []
    tree = NPChunker.parse(sentences)
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            t = subtree
            t = ' '.join(word for word, tag in t.leaves())
            nps.append(t)
    return nps


def sent_parse(input):
    sentences = prepare_text(input)
    nps = parsed_text_to_NP(sentences)
    return nps

def find_nps(text):
    prepared = prepare_text(text)
    parsed = parsed_text_to_NP(prepared)
    #print(parsed)
    return parsed
    #final = sent_parse(parsed)


#nps = find_nps("1 (16 ounce) package cottage cheese")
#print(nps)

measurements = ["ounce", "ounces", "cup", "cups", "quart", "quarts", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "pinch", "dash", "gallon", "gallons", 'package', "packages",
"oz", "qt", "tsp", "tbsp", "gal", "pound", "lb", "ground"]

def get_ingredient(text):
    np_list = find_nps(text)
    for np in np_list:
            #if np==m:
            #    np_list.remove(np)
        if np in measurements:
            np_list.remove(np)

    return np_list


rt = RecipeTransformer()

original = rt.original_recipe("fish and chips")
'''
for item in original:
    print(item)
    print(get_ingredient(item))
'''

print(get_ingredient("eggs"))






#spices taken from https://github.com/dariusk/corpora/tree/master/data/foods
#nlp stuff taken from https://nbviewer.jupyter.org/github/lukewrites/NP_chunking_with_nltk/blob/master/NP_chunking_with_the_NLTK.ipynb