import nltk
import re
import pprint
from nltk import Tree

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
    print(parsed)
    return parsed
    #final = sent_parse(parsed)


#nps = find_nps("1 (16 ounce) package cottage cheese")
#print(nps)
find_nps("1 1/2 (25 ounce) jars tomato-basil pasta sauce")