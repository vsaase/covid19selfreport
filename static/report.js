"use strict";

var options = {
	enableHighAccuracy: true,
	timeout: 3000,
	maximumAge: 0
};

function success(pos) {
	var crd = pos.coords;

	console.log('Your current position is:');
	console.log(`Latitude : ${crd.latitude}`);
	console.log(`Longitude: ${crd.longitude}`);
	console.log(`More or less ${crd.accuracy} meters.`);
	console.log(crd)
	console.log(JSON.stringify({latitude: crd.latitude, longitude: crd.longitude, accuracy: crd.accuracy}))
	document.getElementById("geolocation").value = JSON.stringify({"latitude": crd.latitude, "longitude": crd.longitude, "accuracy": crd.accuracy})
}

function error(err) {
	console.warn(`ERROR(${err.code}): ${err.message}`);
	//alert(err.message);
	//alert("Ihre Ortungsdienste sind für diese Webseite deaktiviert, bitte aktivieren Sie sie, sonst kann kein Bericht erstellt werden.")
	//document.getElementById("geolocation").value = "error"
	//window.location.href = "/";
	if(document.getElementById("geolocation"))
		document.getElementById("geolocation").value = JSON.stringify({"latitude": 0, "longitude": 0, "accuracy": 1})
}

document.addEventListener('DOMContentLoaded', function() {
    navigator.geolocation.getCurrentPosition(success, error, options);
});


$("#report-close-button").on("click", function() {
	$("#report-wrapper").removeClass("active");
	setTimeout(function() {
		$("#report-wrapper").hide();
	}, 500);
});