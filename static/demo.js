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
	
	/*
	map.on('zoomend', function() {
		var zoomlevel = map.getZoom();
		if (zoomlevel < 9){
			if (map.hasLayer(laender_layer)) {
				map.removeLayer(laender_layer);
			} else {
				console.log("no point layer active");
			}
			if (map.hasLayer(kreisareas)) {
				console.log("layer already active");
			} else {
				map.addLayer(kreisareas);
			}
		}else{
			if (map.hasLayer(laender_layer)){
				console.log("layer already added");
			} else {
				map.addLayer(laender_layer);
			}
			if (map.hasLayer(kreisareas)) {
				map.removeLayer(kreisareas);
			} else {
				console.log("no area layer active");
			}
		}
		console.log("Current Zoom Level =" + zoomlevel)
	});
	*/
}

var reportlayer = L.layerGroup();
var rki_layer = L.layerGroup();
var laender_layer = L.layerGroup();
var kreisareas = L.layerGroup();

function onLocationFound(e) {
    var radius = e.accuracy;

    //L.marker(e.latlng).addTo(map)
    //    .bindPopup("You are within " + radius + " meters from this point").openPopup();

    // L.circle(e.latlng, radius).addTo(map);
}


function renderData() {
	var zoomlevel = map.getZoom();

	function onEachFeature(feature, layer) {
		if(feature.properties.risklayer){
			layer.bindTooltip(
				String(feature.properties.risklayer.ncases),
				{
					className: 'tooltip',
					permanent: true, 
					direction:"center",
					opacity: 0.8
				}
			).openTooltip()
		}
	}
	$.getJSON("/static/landkreise_risklayer.geojson", function(data){
		kreisareas =  L.geoJSON(data, {
			onEachFeature: onEachFeature,
			style: function (feature) {
				let s = {
					opacity: 1.0,
					weight:1,
					fillOpacity: 0.8,
					color:"rgb(200,200,200)"
				}
				if(feature.properties.risklayer){
					s.fillColor = feature.properties.risklayer.color;
				}
				return s;
			}
		}).bindPopup(function (layer) {
			if(layer.feature.properties.risklayer){
				return layer.feature.properties.risklayer.popup;
			}else{
				return "keine Daten"
			}
		})
		//if(zoomlevel < 9){
			map.addLayer(kreisareas);
		//}
	});

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
        reportlayer = L.layerGroup(markers);
        map.addLayer(reportlayer);
    });
    $.getJSON("/getrki", function(obj) {
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
        rki_layer = L.layerGroup(markers);
        map.addLayer(rki_layer);
	});
	/*
    $.getJSON("/getlaender", function(obj) {
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
        laender_layer = L.layerGroup(markers);
		if(zoomlevel >= 8){
			map.addLayer(laender_layer);
		}
	});
*/

}


$(function() {
    makeMap();
    map.locate({setView: true, maxZoom: 13});

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend')
        div.innerHTML += '<a href="/report"><img src="/static/add-button.svg" id="fixedbutton"></a>';
        return div;
    };

    legend.addTo(map);

    renderData();
})
