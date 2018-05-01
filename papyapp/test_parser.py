#coding: utf8
import os.path, requests, json, requests_mock
from papyapp import parser


def test_parser():
    os.chdir("/home/rayane/Documents/Save/projet_sept")
    assert parser.parser("Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?") == "OpenClassrooms"
    assert parser.parser("Tu connais pas la tour eiffel?") == "tour eiffel"
    assert parser.parser("montre moi l'arc de triomphe") == "arc triomphe"
    assert parser.parser("où est la Tour Montparnasse") == "Tour Montparnasse"


def test_placeSearch():
    assert parser.placeSearch("voilà un exemple") == "Voilà_Un_Exemple" 

def test_getGeocode(monkeypatch):
    test = {
            "results" : [
                {
                    "address_components" : [
                        {
                            "long_name" : "Nantes",
                            "short_name" : "Nantes",
                            "types" : [ "locality", "political" ]
                        }
                        ],
                    "formatted_address" : "Nantes, France"
                }
                ],
                "status" : "OK"
            }
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock', adapter)
    
    adapter.register_uri('GET', 'mock://maps.googleapis.com/maps/api/geocode/json?', json=test)
    resp = session.get('mock://maps.googleapis.com/maps/api/geocode/json?')

    def mockreturn(request, params):
        return resp

    monkeypatch.setattr(requests, 'get', mockreturn)
    assert parser.getGeocode("tour eiffel") == test


def test_addressSearch():
    test = {
            "results" : [
                {
                    "address_components" : [
                        {
                            "long_name" : "Champ de Mars",
                            "short_name" : "Champ de Mars",
                            "types" : [ "establishment", "point_of_interest" ]
                        }
                        ],
                    "formatted_address" : "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France"
                }
                ],
                "status" : "OK"
            }
    assert parser.addressSearch(test) == "Champ_de_Mars"

def test_getWikiText(monkeypatch):
    test = {
            "batchcomplete": "",
            "query": {
                "pages": {
                    "70864": {
                            "pageid": 70864,
                            "ns": 0,
                            "title": "La Baule-Escoublac",
                            "extract": "La Baule-Escoublac (prononcé /la.bol.ɛs.ku.blak/) est une commune de l'Ouest de la France."
                            }
                        }
                    }
            }
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock', adapter)
    
    adapter.register_uri('GET', 'mock://fr.wikipedia.org/w/api.php?', json=test)
    resp = session.get('mock://fr.wikipedia.org/w/api.php?')
    def mockreturn(request, params):
        return resp

    monkeypatch.setattr(requests, 'get', mockreturn)
    assert parser.getWikiText("La_Baule-Escoublac") == "La Baule-Escoublac (prononcé /la.bol.ɛs.ku.blak/) est une commune de l'Ouest de la France."