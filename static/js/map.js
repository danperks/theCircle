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
        console.log(place.geometry.location);
        document.getElementById("hiddenlocationid").value=place.geometry.location.toString();
        infowindow.open(map, marker);
        
    });
}




async function MapBrowse() { //https://developers.google.com/maps/documentation/javascript/geolocation
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


    const results = await fetchplaces();
    var ArrayOfPlaceID = ['Eh1BZGVsYWlkZSBTdCwgQ292ZW50cnkgQ1YxLCBVSyIuKiwKFAoSCc8WV_S_S3dIEWZmR37TBd78EhQKEgmpkcdCETtaAhF6JYgyQ6D4xA','ChIJcUPaFltKd0gRXVDAnM3WjVA']

    for(i = 0;i<Object.keys(results).length;i++){
    var request = {
        placeId: results[i]
    };
    var service = new google.maps.places.PlacesService(map);
    service.getDetails(request, function(place, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
          var marker = new google.maps.Marker({
            map: map,
            position: place.geometry.location
          });
        }});
    }
    



    /* var markerlan2 = new google.maps.LatLng(ArrayOfLats[0], ArrayOfLongs[0]);
    var marker2 = new google.maps.Marker({
        position: markerlan2,
        map:map,
        title:"Hello World!"
        
    }); */
    
    




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
        
        //document.getElementById("hiddenplaceid").value =ExportPlaceID;
        infowindow.open(map, marker);
        
    });
    
}

async function fetchplaces(){
    const res = await fetch('api/fetchplaces', {
        method: 'get',
        
    });
    const estimation = await res.json()
    
    return estimation;
}
