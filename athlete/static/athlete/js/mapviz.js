var map;
var gpxurl;
var x = document.getElementById("gpxPlot");
var points = [];
// Starting geolocation of the GPX file
var lat_start = [];
var lon_start = [];
// Ending geolocation of the GPX file
var lat_stop = [];
var lon_stop = [];
// For shutting down recording:
var centerLocation;

var gpx_latitude = [];
var gpx_longitude = [];
var gpx_elevation = [];
var gpx_distance = [];

var next_button_value = -1;
var distanceSegment = 20; // TAken from Python. Needs modification to autogenerate this value from python
var markers = [];

function markGoogleMap(x0){
    deleteMarkers(); // Delete previous markers
    // NOTE: https://developers.google.com/maps/documentation/javascript/examples/marker-remove
    // Identify latitude, lingitude corresponding to x0
    for (var i=0; i<gpx_distance.length; i++){
        if(x0 <= gpx_distance[i]){
            var marker = new google.maps.Marker({
                position: {lat: gpx_latitude[i], lng: gpx_longitude[i]},
                map: map,
            });
            markers.push(marker);
            // setAllMarker(map);
            break;
        }
    }
}

// Sets the map on all markers in the array.
function setAllMarker(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  setAllMarker(null);
  markers = [];
}

function getMap() { 
    map = new google.maps.Map(document.getElementById('gpxPlot'), {
        center: centerLocation,
        zoom: 9
    });
}

function getRouteOnMap() {
    var poly = new google.maps.Polyline({
            // use your own style here
            path: points,
            strokeColor: "#FF00AA",
            strokeOpacity: .7,
            strokeWeight: 4
        });
            poly.setMap(map);
}

$(document).on("pageinit", "#googlemapPlot", function(event){
    gpxurl = String($(this).data('gpxurl'));
    route_extraction();
});
    
// Extraction of route info from the rider's entered gpx file
function route_extraction(){
    console.log("1. route_extraction activated");
    $.ajax({
        type: "GET",
        url: gpxPlotGraph,
        success: function(data){
            for (var i = 0; i < data.length; i++) {
                gpx_latitude.push(data[i]['latitude']);
                gpx_longitude.push(data[i]['longitude']);
                gpx_elevation.push(data[i]['elevation']);
                gpx_distance.push(data[i]['distance']);
            }
            console.log(gpx_latitude[0]);
            lat_start = gpx_latitude[0];
            lon_start = gpx_longitude[0];
            lat_stop = gpx_latitude[gpx_distance.length-1];
            lon_stop = gpx_longitude[gpx_distance.length-1];
            for (i=0; i<gpx_distance.length; i++){
                var p = new google.maps.LatLng({lat: gpx_latitude[i], lng: gpx_longitude[i]}); 
                points.push(p);
            }
            centerLocation = new google.maps.LatLng({lat: lat_start, lng: lon_start});
            getMap();
            getRouteOnMap(); // AJAX successful call takes time. Hence calling getRouteOnMap() only after a successful call.
            d3js_graph_plotting_area();
        }
    });
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

// D3js

function d3js_graph_plotting_area(){

    // LINK: https://bl.ocks.org/d3noob/23e42c8f67210ac6c678db2cd07a747e
    // LINK for area: https://bl.ocks.org/mbostock/3883195

    // Set the dimension
    var margin = {top: 20, right: 20, bottom: 50, left: 70},
                    width = 1300 - margin.left - margin.right,
                    height = 300 - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // Define the area
    var valueline = d3.area()
                        .x(function(d) { return x(d.x); })
                        .y0(height)
                        .y1(function(d) { return y(d.y); });

    bisectDistance = d3.bisector(function(d) { return d.x; }).left;

    // Define the div for the tooltip
    // NOTE: http://bl.ocks.org/d3noob/a22c42db65eb00d4e369
    var tooltip = d3.select("#d3js_Plot").append("div")
                                .attr("class", "tooltip")               
                                .style("opacity", 0);

    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#d3js_Plot").append("svg")
                                .attr("width", width + margin.left + margin.right)
                                .attr("height", height + margin.top + margin.bottom)
                                .append("g")
                                .attr("transform",
                                        "translate(" + margin.left + "," + margin.top + ")");

    // Get the data
    // NOTE: http://stackoverflow.com/questions/920930/how-to-create-json-by-javascript-for-loop
    var min_elevation = Math.min.apply(Math, gpx_elevation);
    var max_elevation = Math.max.apply(Math, gpx_elevation) - min_elevation;
    var Data = [];
    for (var i in gpx_distance){
        Data.push({
            "x": gpx_distance[i],
            "y": gpx_elevation[i]-min_elevation,
            "lat": gpx_latitude,
            "lon": gpx_longitude
    });
    }

    // Scale the range of the data
    // NOTE: http://stackoverflow.com/questions/4020796/finding-the-max-value-of-an-attribute-in-an-array-of-objects
    var max_xValue = Math.max.apply(Math,Data.map(function(o){return o.x;}));
    var max_yValue = Math.max.apply(Math,Data.map(function(o){return o.y;}));
    x.domain([0, max_xValue]);
    y.domain([0, max_elevation+30]);

    // Add the valueline path.
    svg.append("path")
        .data([Data])
        //.attr("class", "line")
        .attr("d", valueline)
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("fill", "lightsteelblue");

    var focus = svg.append("g") 
                    .style("display", "none");

    // append the circle at the intersection 
    focus.append("circle")
            .attr("class", "y")
            .style("fill", "none")
            .style("stroke", "red")
            .attr("r", 6);

    // Vertical line
    var verticalLine = svg.append("line")
                            .style("stroke-width", 1)
                            .style("stroke", "blue")
                            .style("fill", "none");


    svg
        .on("mouseover", function(d){
            var x0 = x.invert(d3.mouse(this)[0]);  
            var y0 = y.invert(d3.mouse(this)[1]); 
            // console.log(x0, y0);
            markGoogleMap(x0);
            tooltip.transition()        
                    .duration(200)      
                    .style("opacity", .9);
            tooltip.html("Dist:  " + Math.round(x0 * 100) / 100 + "<br/>"  + "Elev:  " + Math.round(y0 * 100) / 100)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY-40) + "px");
            focus.style("display", null);
            verticalLine.style("stroke-width", 0);
        })
        .on("mouseout", function(d) { 
            deleteMarkers();      
            tooltip.transition()        
                .duration(500)      
                .style("opacity", 0); 
            focus.style("display", "none");
            verticalLine.style("stroke-width", 0);
        })
        // NOTE: http://bl.ocks.org/d3noob/e5daff57a04c2639125e
        .on("mousemove", function(d) {       
            var x0 = x.invert(d3.mouse(this)[0]); 
            var i = bisectDistance(Data, x0, 1);
            var d1 = Data[i];
            var y0 = d1.y;
            var mouseX = d3.mouse(this)[0];
            var mouseY = y(y0);

            tooltip.transition()        
                    .duration(200)      
                    .style("opacity", .9);
            tooltip.html("Dist:  " + Math.round(x0 * 100) / 100 + "<br/>"  + "Elev:  " + Math.round(d1.y * 100) / 100)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY-40) + "px"); 

            markGoogleMap(x0)
            focus.select("circle.y")
                    .attr("transform",
                        "translate(" + x(d1.x) + "," +
                                         y(d1.y) + ")");
            verticalLine
                    .attr("x1", mouseX)  //<<== change your code here
                    .attr("y1", height)
                    .attr("x2", mouseX)  //<<== and here
                    .attr("y2", mouseY)
                    .style("stroke-width", 1);
            // ISSUE: Old lines remain in its position

        });
    

    // Add the x Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // text label for the x axis
    svg.append("text")             
        .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
        .style("text-anchor", "middle")
        .text("Distance (km)");

    // Add the y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    // text label for the y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Elevation (m)");      
}