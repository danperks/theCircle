// This sample uses the Place Autocomplete widget to allow the user to search
// for and select a place. The sample then displays an info window containing
// the place ID and other information about the place that the user has
// selected.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
var ExportPlaceID = 0;

function initMap() { //https://developers.google.com/maps/documentation/javascript/geolocation
    var map, infoWindow;
    var map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 51.841100, lng: -30.508039 },
        zoom: 13,
        streetViewControl: false,
        fullscreenControl: false,
        mapTypeControl: false
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            }
            map.setCenter(new google.maps.LatLng(pos.lat, pos.lng));
        })
    };








    var input = document.getElementById('pac-input');

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    // Specify just the place data fields that you need.
    autocomplete.setFields(['place_id', 'geometry', 'name']);

    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var infowindow = new google.maps.InfoWindow();
    var infowindowContent = document.getElementById('infowindow-content');
    infowindow.setContent(infowindowContent);

    var marker = new google.maps.Marker({ map: map });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
        console.log("ins")
    });
    
    autocomplete.addListener('place_changed', function() {
        
        infowindow.close();

        var place = autocomplete.getPlace();

        if (!place.geometry) {
            return;
        }

        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        // Set the position of the marker using the place ID and location.
        marker.setPlace({
            placeId: place.place_id,
            location: place.geometry.location
        });

        marker.setVisible(true);

        infowindowContent.children['place-name'].textContent = place.name;
        infowindowContent.children['place-id'].textContent = place.place_id;
        infowindowContent.children['place-address'].textContent =
            place.formatted_address;
        
        ExportPlaceID = place.place_id;
        console.log(ExportPlaceID)
        
        document.getElementById("hiddenplaceid").value =ExportPlaceID;
        infowindow.open(map, marker);
        
    });
}




function MapBrowse() { //https://developers.google.com/maps/documentation/javascript/geolocation
    var map, infoWindow;
    var map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 51.841100, lng: -30.508039 },
        zoom: 13,
        streetViewControl: false,
        fullscreenControl: false,
        mapTypeControl: false
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            }
            map.setCenter(new google.maps.LatLng(pos.lat, pos.lng));
        })
    };








    var input = document.getElementById('pac-input');

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    //Specify just the place data fields that you need.
    autocomplete.setFields(['place_id', 'geometry', 'name']);

    //map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var infowindow = new google.maps.InfoWindow();
    var infowindowContent = document.getElementById('infowindow-content');
    infowindow.setContent(infowindowContent);

    var marker = new google.maps.Marker({ map: map });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
        console.log("ins")
    });
    
    autocomplete.addListener('place_changed', function() {
        
        infowindow.close();

        var place = autocomplete.getPlace();

        if (!place.geometry) {
            return;
        }

        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        // Set the position of the marker using the place ID and location.
        marker.setPlace({
            placeId: place.place_id,
            location: place.geometry.location
        });

        marker.setVisible(true);

        infowindowContent.children['place-name'].textContent = place.name;
        infowindowContent.children['place-id'].textContent = place.place_id;
        infowindowContent.children['place-address'].textContent =
            place.formatted_address;
        
        ExportPlaceID = place.place_id;
        console.log(ExportPlaceID)
        
        document.getElementById("hiddenplaceid").value =ExportPlaceID;
        infowindow.open(map, marker);
        
    });
}