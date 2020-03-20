$(document).ready(function() {

	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				userSearch : $('#addressInput').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			//console.log(document.getElementById("story").textContent);
			if (data.error) {
				$('#addressInput').text(data.error);
			}
			else {
				$('#gmap').attr('src',"https://maps.googleapis.com/maps/api/staticmap?markers=color:blue|label:S|".concat(data.lat).concat(data.lng).concat("&zoom=17&size=300x300&key=AIzaSyAbx36JQ_EiREnYBSAY2CzfiJaQHGBGhD8"));
				$('#story').prepend("<div class=\"w3-container w3-light-grey\"></div>");
				$('#story').prepend("<div class=\"w3-container w3-grey\"></div>");
				document.getElementById("story").childNodes[0].textContent = data.inputText;
				document.getElementById("story").childNodes[1].textContent = data.message.concat(data.address).concat(data.papyStory);
				document.getElementById("displayer").style.height = "400px";
			}

		});

		event.preventDefault();

	});

});