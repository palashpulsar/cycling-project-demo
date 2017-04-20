var map;

var gpx_latitude = [];
var gpx_longitude = [];
var gpx_elevation = [];
var gpx_distance = [];

var next_button_value = -1;
var distanceSegment = 20; // TAken from Python. Needs modification to autogenerate this value from python
var markers = [];

$(document).on("pageinit", "#googlemapPlot", function(event){
    route_extraction();
});
    
// Extraction of route info from the rider's entered gpx file
function route_extraction(){
    console.log("1. route_extraction activated");
    var points = [];
    $.ajax({
        type: "GET",
        url: gpxPlotGraph,
        success: function(data){
            console.log(data['latitude']);
            gpx_latitude = data['latitude'];
            gpx_longitude = data['longitude'];
            gpx_elevation = data['elevation']; 
            gpx_distance = data['distance'];
            var lat_start = gpx_latitude[0];
            var lon_start = gpx_longitude[0];
            for (var i=0; i<gpx_distance.length; i++){
                var p = new google.maps.LatLng({lat: gpx_latitude[i], lng: gpx_longitude[i]}); 
                points.push(p);
            }
            var centerLocation = new google.maps.LatLng({lat: lat_start, lng: lon_start});
            getMap(centerLocation);
            getRouteOnMap(points); // AJAX successful call takes time. Hence calling getRouteOnMap() only after a successful call.
            [svg, Data, margin, height, width, x, y] = svgPlot();
            // getPreviousDistanceMarked(svg, height, Data, x, y);
            mouseHovering(svg);
        }
    });
}

function getMap(centerLocation) {
    console.log("2. I am inside getMap");
    map = new google.maps.Map(document.getElementById('gpxPlot'), {
        center: centerLocation,
        zoom: 9
    });
}

function getRouteOnMap(points) {
    console.log("3. I am inside getRouteOnMap");
    var poly = new google.maps.Polyline({
            // use your own style here
            path: points,
            strokeColor: "#FF00AA",
            strokeOpacity: .7,
            strokeWeight: 4
        });
            poly.setMap(map);
}

// Generating csrftoken 
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};