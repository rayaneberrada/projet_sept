from papyapp import app, parser
from flask import render_template, request, jsonify
import json, requests, random

@app.route("/")
def mainpage():
	return render_template("mainpage.html")

@app.route("/process", methods=["POST"])
def getMap():
	userSearch = request.form["userSearch"]
	message = parser.choseMessage()
	placeToSearch = parser.parser(userSearch)
	geocode = parser.getGeocode(placeToSearch)
	if not geocode["results"]:
		"""
		If the google map API doesn't return any informations about the place searched by the user
		"""
		message = "Désolé je n'ai pas compris votre message.Pourriez vous être plus clair?(vérifiez l'orthographe du lieu ou la formulation de la question)"
		papyText = ""
		lat = ""
		lng = ""
		addressAPI = ""
	else:
		"""
		If the google map API return informations about the place, they are added to the json data
		sent by the user so that they can be added to the page with ajax
		"""
		addressAPI = geocode["results"][0]["formatted_address"] + "."
		lat = str(geocode["results"][0]["geometry"]["location"]["lat"]) + ","
		lng = str(geocode["results"][0]["geometry"]["location"]["lng"])
		firstSearch = parser.placeSearch(placeToSearch)
		papyText = parser.getWikiText(firstSearch)
		#Try to search wikipedia informations with the name of the place written by the user
		if papyText == False:
			#If no informations have been found on the wiki media API, it search again with the address returned by the google map API
			secondSearch = parser.addressSearch(geocode)
			papyText = parser.getWikiText(secondSearch)
			print("secondSearch", secondSearch)
			if papyText == False:
				#If no informations returned with the address from the google map API, display that error message
				message = "Désolé mais je n'ai trouvé qu'une adresse pour ce lieu:"
				papyText = ""
	return jsonify({"inputText" : userSearch, "message" : message, "papyStory" : papyText,"address" : addressAPI, "lat" : lat, "lng" : lng })