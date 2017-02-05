var map;
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
var icon_markers = [];
var gpx_latitude = [];
var gpx_longitude = [];
var gpx_elevation = [];
var gpx_distance = [];
var roadColor = "#9E9E9E";
var drivenRoadColor = "#037DD7";
var next_button_value = -1;
var distanceSegment = 20; // TAken from Python. Needs modification to autogenerate this value from python
var markers = [];
var markersRide = [];
var drivenRoad = [];

function markGoogleMap(x0){
    deleteMarkers(); // Delete previous markers
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
    console.log("I am inside getMap function");
    map = new google.maps.Map(document.getElementById('gpxPlot'), {
        center: centerLocation,
        zoom: 9
    });
    drivenRoad = new google.maps.Polyline({
        map: map,
        path: [],
        strokeColor: drivenRoadColor,
        strokeOpacity: 1,
        strokeWeight: 3
    });
}

function getRouteOnMap() {
    console.log("I am inside getRouteOnMap function");
    var poly = new google.maps.Polyline({
            // use your own style here
            path: points,
            strokeColor: roadColor,
            strokeOpacity: 1,
            strokeWeight: 4
        });
            poly.setMap(map);
}

$(document).on("pageinit", "#googlemapPlot", function(event){
    console.log(audioHistory);
    route_extraction();
});
    
// Extraction of route info from the rider's entered gpx file
function route_extraction(){
    console.log("1. route_extraction activated");
    $.ajax({
        type: "GET",
        url: csvPlotGraph,
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
            [svg, Data, margin, height, width, x, y] = svgPlot();
            getPreviousDistanceMarked(svg, height, Data, x, y);
            mouseHovering(svg);
            drawDrivenRoad();
        }
    });
}

function svgPlot(){

    //PART 1
    console.log("I am inside svg.");

    // Set the dimension
    var margin = {top: 20, right: 20, bottom: 50, left: 70},
                    width = 1300 - margin.left - margin.right,
                    height = 300 - margin.top - margin.bottom;

    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#d3js_Plot").append("svg")
                                .attr("width", width + margin.left + margin.right)
                                .attr("height", height + margin.top + margin.bottom)
                                .append("g")
                                .attr("transform",
                                        "translate(" + margin.left + "," + margin.top + ")");
    // PART 2
    // Get the data
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

    // Set the ranges
    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // Scale the range of the data
    var max_xValue = Math.max.apply(Math,Data.map(function(o){return o.x;}));
    var max_yValue = Math.max.apply(Math,Data.map(function(o){return o.y;}));
    x.domain([0, max_xValue]);
    y.domain([0, max_elevation+30]);


    // Define the area
    var valueline = d3.area()
                        .x(function(d) { return x(d.x); })
                        .y0(height)
                        .y1(function(d) { return y(d.y); });

    // Add the valueline path.
    svg.append("path")
        .data([Data])
        //.attr("class", "line")
        .attr("d", valueline)
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("fill", "lightsteelblue");

    // Vertical line
    var verticalLine = svg.append("line")
                            .style("stroke-width", 1)
                            .style("stroke", "blue")
                            .style("fill", "none");

    // No idea what this is
    // Position of Vertical lIne
    var posTopLine = $('svg').position().top + margin.top;
    var heightLine = 300;

    // PART 3
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

    return [svg, Data, margin, height, width, x, y];
}

function getPreviousDistanceMarked(svg, height, Data, x, y){
    console.log("I am in getPreviousDistanceMarked function");
    var imageOffsetX = 10;
    var imageOffsetY = 20; 
    bisectDistance = d3.bisector(function(d) { return d.x; }).left;

    var markedDistance = locatePreviousHistory();

    for(var i=0; i<markedDistance.length; i++){
        var x0 = markedDistance[i];
        var mouseX = x(x0);            
        var k = bisectDistance(Data, x0, 1);
        var y0 = Data[k].y;
        var mouseY = y(y0);
        var verticalLine = svg.append("line")
                                .style("stroke-width", 1)
                                .style("stroke", "black")
                                .style("fill", "none")
                                .attr("x1", mouseX)  //<<== change your code here
                                .attr("y1", height)
                                .attr("x2", mouseX)  //<<== and here
                                .attr("y2", mouseY);
        var img = svg.append("svg:image")
                    .attr("xlink:href", audioImagePath)
                    .attr("width", 15)
                    .attr("height", 15)
                    .attr("x", mouseX - imageOffsetX)
                    .attr("y", mouseY - imageOffsetY)
        }                       
}

function mouseHovering(svg){
    console.log("I am inside mouseHovering");
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

    // Define the div for the tooltip
    var tooltip = d3.select("#d3js_Plot").append("div")
                                .attr("class", "tooltip")               
                                .style("opacity", 0);

    svg
        .on("mouseover", function(d){
            var x0 = x.invert(d3.mouse(this)[0]);  
            var y0 = y.invert(d3.mouse(this)[1]); 
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

    // On Click, pop up appears
    svg.on("click", function() {
        var imageOffsetX = 10;
        var imageOffsetY = 20; 
        var mouseX = d3.mouse(this)[0];
        var x0 = x.invert(d3.mouse(this)[0]);
        var i = bisectDistance(Data, x0, 1);
        var y0 = Data[i].y;
        var mouseY = y(y0);
        // Identify latitude, lingitude corresponding to x0
        saveAudio(x0);
        addSoundIcon(x0);        
        var verticalLine = svg.append("line")
                                .attr("x1", mouseX)  //<<== change your code here
                                .attr("y1", height)
                                .attr("x2", mouseX)  //<<== and here
                                .attr("y2", mouseY)
                                .style("stroke-width", 1)
                                .style("stroke", "black")
                                .style("fill", "none");
        var img = svg.append("svg:image")
                    .attr("xlink:href", audioImagePath)
                    .attr("width", 15)
                    .attr("height", 15)
                    .attr("x", mouseX - imageOffsetX)
                    .attr("y", mouseY - imageOffsetY)
        // modal.style.display = "block";
        // modal_function(Math.round(x0 * 100) / 100, svg, mouseX, mouseY, imageOffsetX, imageOffsetY);
    });
}

function saveAudio(x0){
    console.log("saveAudio function activated. URL called: " + audioSave);
    for (var i=0; i<gpx_distance.length; i++){
        if (x0 <= gpx_distance[i]){
            var dis_Mark_Pos = i;
            break;
        }
    }
    var dis_Mark = x0;
    var dis_lat = gpx_latitude[dis_Mark_Pos];
    var dis_lon = gpx_longitude[dis_Mark_Pos];
    console.log(dis_lat);
    var data = {dis_Mark: dis_Mark, dis_Mark_Pos: dis_Mark_Pos, dis_lat: dis_lat, 
        dis_lon: dis_lon, csrfmiddlewaretoken : getCookie('csrftoken')};
    $.post(audioSave, data, function(response){
    });
}

function addSoundIcon(x0){
    console.log("   a. addSoundIcon function activated");
    for (var i=0; i<gpx_distance.length; i++){
        if(x0 <= gpx_distance[i]){
            var lat_clicked = gpx_latitude[i];
            var lon_clicked = gpx_longitude[i];
            break;
        }
    }
    var icon = {
        path: 'M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z',
        fillColor: roadColor,
        fillOpacity: 0.8,
        scale: 0.8,
    };
    var icon_marker = new google.maps.Marker({
        position: {lat: lat_clicked, lng: lon_clicked},
        icon: icon,
        map: map
    });
    icon_markers.push(icon_marker);
}

function locatePreviousHistory(){
    console.log("I am inside locatePreviousHistory function.");
    var markedDistance = [];
    $.ajax({
        type: "GET",
        url: audioHistory,
        async: false,
        success: function(data){
            for (var i = 0; i < data.length; i++) {
                markedDistance.push(data[i]);
                addSoundIcon(data[i]);
            }                
        }
    });
    console.log("markedDistance: " + markedDistance);
    return markedDistance;
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

// Stage 2: For live tracking
// Get the driven path on the map
function drawDrivenRoad(){
    console.log("I am in drawDrivenRoad function");
    console.log(retrieveDrivenGeo);
    var drivenLatitude = null;
    var drivenLongitude = null;
    $.ajax({
        type: "GET",
        url: retrieveDrivenGeo,
        success: function(data){
            console.log(data['latitude'].length);
            for (var i = 0; i < data['latitude'].length; i++) {
                drivenLatitude = parseFloat(data['latitude'][i]);
                drivenLongitude = parseFloat(data['longitude'][i]);
                console.log(drivenLatitude + ", " + drivenLongitude);
                console.log(typeof drivenLatitude);
                var path = drivenRoad.getPath();
                path.push(new google.maps.LatLng(drivenLatitude, drivenLongitude));         
            }
            drivenRoad.setPath(path);
            updateRiderMarker(drivenLatitude, drivenLongitude);
        }
    });
}

// Update market
function updateRiderMarker(drivenLatitude, drivenLongitude){
    console.log("   a. updateMarker function activated");
    deleteRiderMarkers();
    var marker = new google.maps.Marker({
        position: {lat: drivenLatitude, lng: drivenLongitude},
        label: 'PS',
        map: map,
        title: 'Hello World!'
    });
    markersRide.push(marker);
    map.panTo({lat: drivenLatitude, lng: drivenLongitude});
}
// Deletes all markers in the array by removing references to them.
function deleteRiderMarkers() {
    console.log("   b. deleteMarkers function activated");
    setAllRiderMarker(null);
    markersRide = [];
}
// Sets the map on all markers in the array.
function setAllRiderMarker(map) {
    console.log("   c. setAllMarker function activated");
    for (var i = 0; i < markersRide.length; i++) {
        markersRide[i].setMap(map);
    }
}