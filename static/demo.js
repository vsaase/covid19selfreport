BASECOORDS = [51.3150172,9.3205287];

var blueIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var goldIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var redIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var greenIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var orangeIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var yellowIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var violetIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var greyIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var blackIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
	shadowUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

function onLocationError(e) {
    //alert(e.message);
}

function makeMap() {
    var TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var MB_ATTR = 'Ein Forschungsprojekt der Medizinischen Fakultät Mannheim der Universität Heidelberg. <a href="/info">Informationen zum Projekt und Spendenaufruf</a>, <a href="/impressum">Impressum</a>,  <a href="/delete">Daten löschen</a>, Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    map = L.map('map').setView(BASECOORDS, 6);
    map.on('locationfound', onLocationFound);
    map.on('locationerror', onLocationError);
    L.tileLayer(TILE_URL, {attribution: MB_ATTR}).addTo(map);
}

var layer = L.layerGroup();

function onLocationFound(e) {
    var radius = e.accuracy;

    //L.marker(e.latlng).addTo(map)
    //    .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
}


function renderData() {
    $.getJSON("/getreports", function(obj) {
        var markers = obj.coords.map(function(arr) {
            var icon = greenIcon;
            if(arr["test"]=="Positiv"){
                icon = orangeIcon;
            }
            let marker = L.marker([arr["latitude"], arr["longitude"]], {icon: icon})
            marker.bindPopup('<p>'+arr["date"]+'<br/>' + arr["symptoms"] + '<br/>seit ' + arr["dayssymptoms"] + ' Tagen<br/>' + arr["nothers"] + ' Bekannte mit Symptomen<br/>Virustest: ' + arr["test"] + '</p>')
            return marker;
        });
        //map.removeLayer(layer);
        layer = L.layerGroup(markers);
        map.addLayer(layer);
    });
    $.getJSON("/getsimulations", function(obj) {
        var markers = obj.coords.map(function(arr) {
			var icon = redIcon
			if(arr["ncases"] == 0){
				icon = blackIcon
			}
			if(arr["source"] == "RKI"){
				icon = blueIcon
			}
            let marker = L.marker([arr["latitude"], arr["longitude"]], {icon: icon})
            marker.bindPopup(arr["popup"])
            return marker;
        });
        //map.removeLayer(layer);
        layer = L.layerGroup(markers);
        map.addLayer(layer);
    });
}


$(function() {
    makeMap();
    map.locate({setView: true, maxZoom: 16});

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend')
        div.innerHTML += '<a href="/report"><img src="/static/add-button.svg" id="fixedbutton"></a>';
        return div;
    };

    legend.addTo(map);

    renderData();
})
