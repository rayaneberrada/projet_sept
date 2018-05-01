# -*- coding: utf-8 -*-0
import random
import json
import requests


def parser(data):
    """
    the parser function will remove from the sentence written by the user all
    the words contained in the words_to_remove list, all the words which match 
    the ones in the file stopword.json and remove all the words written before
    a word contained before certains words
    """
    for letter in data:
        if letter in (",", ".", "'", "?", "!"):
            data = data.replace(letter, " ")
    #replace ponctuation with spaces

    address = data.split()
    #create a list containing the adress

    with open("papyapp/stopword.json") as f:
        stop_word_file = json.load(f)

    words_to_remove = ["stp", "s'il vous plait", "s'il te plait", "s'il vous plaît",\
                     "s'il te plaît", "papy", "grandPy", "Grandpy", "grandpy", "GrandPy"]
    #list of words removed from the adress list

    words_to_compare = ["adresse", "connais", "connai", "connaissez-vous", \
                        "connais-tu", "savez-vous", "sais-tu", "ou", "où", "est",\
                         "voir", "afficher", "affiches", "affiche", "montre", "montrer",\
                          "veux", "trouve", "sais tu", "savez vous"]
    """
    List of words used to compare with the address list
    """

    for word in address[:]:
        for stopword in words_to_compare:
            if stopword in address:
                if  address.index(word) <= address.index(stopword):
                    words_to_remove.append(word)
            words_to_remove.append(stopword)
    """
    If one of the words of the list words_to_compare exist in the lsit address,
    all the words that have a smaller index (so it means where before in the string address before
    it was changed into a list) are added to the list words_to_remove
    """
    
    for word in address[:]:
        if word in stop_word_file or word in words_to_remove:
            address.remove(word)
    print(address)
    return ' '.join(address)

def choseMessage():
    """
    Chose a random message to be displayed by GrandPy
    """
    message = ["Aussitôt dis aussitôt fait: ", "Abracadabra: ", "D'après ma boule de cristal: ",\
                "Après un coup d'oeuil sur ma vieille carte, je dirai: ", "Ici mon poussin: "]
    message = random.choice(message)
    #voir methode choice de random
    return message


def getGeocode(data):
    """
    Get a json file from the google map API containing informations about the adress 
    of the place searched by the user
    """
    parameters = {"address": data, "key":"AIzaSyCYO19C5Kv2Q2ofylRVEnU2KS5PZYa6e3o"}
    geocodeJson = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=parameters)
    geocode = geocodeJson.json()
    return geocode

def placeSearch(data):
    """
    Return a string adapted for the wikipedia API based on the place searched by the user
    """
    data = data.split()
    print(data)
    search = ""
    for word in data:
        neWord = str(word[:1].upper() + word[1:])
        if word == data[0]:
            search = neWord
        else:
            search = search + "_" + neWord
        print(search)
    return search


def addressSearch(data):
    """
    Return a string adapted for the wikipedia API based on the address of the placed searched by the user
    """
    wikiSearch = None
    for info in data["results"][0]["address_components"]:
        if info["types"][0] in ["establishment", "route", "locality", "administrative_area_level_2",\
                                 "neighborhood", "point_of_interest"]:
            wikiSearch = info['long_name']
            wikiSearch = wikiSearch.replace(" ", "_")
            break
    return wikiSearch

def getWikiText(data):
    """
    Get a json file from the Wikipedia API containing text about a place searched
    """
    parameters = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": data,
        "utf8": 1,
        "exsentences": "4",
        "explaintext": 1,
        "exsectionformat": "plain",
        "excontinue": ""
    }
    wikiTextJson = requests.get('https://fr.wikipedia.org/w/api.php?', params=parameters)
    wikiText = wikiTextJson.json()
    pageId = list(wikiText["query"]["pages"].keys())[0]
    if pageId == "-1":
        papyText = False
    else:
        papyText = wikiText["query"]["pages"][pageId]["extract"]
    return papyText
