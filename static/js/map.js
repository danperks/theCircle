// This sample uses the Place Autocomplete widget to allow the user to search
// for and select a place. The sample then displays an info window containing
// the place ID and other information about the place that the user has
// selected.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

// This is actually a mess
let ExportPlaceID = 0;

function initMap() { // https://developers.google.com/maps/documentation/javascript/geolocation
  let map;
  let infoWindow;
  map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 51.841100, lng: -30.508039 },
    zoom: 13,
    streetViewControl: false,
    fullscreenControl: false,
    mapTypeControl: false,
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      map.setCenter(new google.maps.LatLng(pos.lat, pos.lng));
    });
  }

  const input = document.getElementById('pac-input');

  const autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo('bounds', map);

  // Specify just the place data fields that you need.
  autocomplete.setFields(['place_id', 'geometry', 'name']);

  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  const infowindow = new google.maps.InfoWindow();
  const infowindowContent = document.getElementById('infowindow-content');
  infowindow.setContent(infowindowContent);

  const marker = new google.maps.Marker({ map });

  marker.addListener('click', () => {
    infowindow.open(map, marker);
    console.log('ins');
  });

  autocomplete.addListener('place_changed', () => {
    infowindow.close();

    const place = autocomplete.getPlace();

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
      location: place.geometry.location,
    });

    marker.setVisible(true);

    infowindowContent.children['place-name'].textContent = place.name;
    infowindowContent.children['place-id'].textContent = place.place_id;
    infowindowContent.children['place-address'].textContent = place.formatted_address;

    ExportPlaceID = place.place_id;
    console.log(ExportPlaceID);

    document.getElementById('hiddenplaceid').value = ExportPlaceID;
    console.log(place.geometry.location);
    document.getElementById('hiddenlocationid').value = place.geometry.location.toString();
    infowindow.open(map, marker);
  });
}

let results;

async function MapBrowse (){
  var map; let
    infoWindow;
  var map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 51.841100, lng: -30.508039 },
    zoom: 13,
    streetViewControl: false,
    fullscreenControl: false,
    mapTypeControl: false,
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      map.setCenter(new google.maps.LatLng(pos.lat, pos.lng));
    });
  }

  results = await fetchplaces();
  console.log(results);
  const ArrayOfPlaceID = ['Eh1BZGVsYWlkZSBTdCwgQ292ZW50cnkgQ1YxLCBVSyIuKiwKFAoSCc8WV_S_S3dIEWZmR37TBd78EhQKEgmpkcdCETtaAhF6JYgyQ6D4xA', 'ChIJcUPaFltKd0gRXVDAnM3WjVA'];

  for (i = 0; i < Object.keys(results).length; i++) {
    const request = {
      placeId: results[i],
    };
    const service = new google.maps.places.PlacesService(map);
    service.getDetails(request, (place, status) => {
      if (status == google.maps.places.PlacesServiceStatus.OK) {
          addtosidesidebar(place.name,'/putALinkInMe',false)
        const marker = new google.maps.Marker({
          map,
          position: place.geometry.location,
        });
      }
    });
  }

  /* var markerlan2 = new google.maps.LatLng(ArrayOfLats[0], ArrayOfLongs[0]);
    var marker2 = new google.maps.Marker({
        position: markerlan2,
        map:map,
        title:"Hello World!"

    }); */

  const input = document.getElementById('pac-input');

  const autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo('bounds', map);

  // Specify just the place data fields that you need.
  autocomplete.setFields(['place_id', 'geometry', 'name']);

  // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  const infowindow = new google.maps.InfoWindow();
  const infowindowContent = document.getElementById('infowindow-content');
  infowindow.setContent(infowindowContent);

  const marker = new google.maps.Marker({ map });

  marker.addListener('click', () => {
    infowindow.open(map, marker);
    console.log('ins');
  });

  autocomplete.addListener('place_changed', () => {
    infowindow.close();

    const place = autocomplete.getPlace();

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
      location: place.geometry.location,
    });

    marker.setVisible(true);

    infowindowContent.children['place-name'].textContent = place.name;
    infowindowContent.children['place-id'].textContent = place.place_id;
    infowindowContent.children['place-address'].textContent = place.formatted_address;

    ExportPlaceID = place.place_id;
    console.log(ExportPlaceID);

    // document.getElementById("hiddenplaceid").value =ExportPlaceID;
    infowindow.open(map, marker);
  });
};

function addGap() {
  const nav = document.getElementById('sidenav');
  const li = document.createElement('li');
  const a = document.createElement('a');
  li.appendChild(a);
  const i = document.createElement('i');
  a.appendChild(i);
  const p = document.createElement('p');
  a.appendChild(p);
  nav.appendChild(li);
}

function addtosidesidebar(text, href, bad) {
  nav = document.getElementById('sidenav');
  li = document.createElement('li');
  a = document.createElement('a');
  if (bad) {
    a.style.color = '#f0342e';
  }
  a.href = href;
  li.appendChild(a);
  i = document.createElement('i');
  i.className = 'now-ui-icons location_pin';
  a.appendChild(i);
  p = document.createElement('p');
  p.innerHTML = text;
  a.appendChild(p);
  nav.appendChild(li);
}

function addtosidesidebarerror(text, bad) {
  nav = document.getElementById('sidenav');
  li = document.createElement('li');
  a = document.createElement('a');
  if (bad) {
    a.style.color = '#f0342e';
  }
  li.appendChild(a);
  i = document.createElement('i');
  i.className = 'now-ui-icons ui-1_simple-remove';
  a.appendChild(i);
  p = document.createElement('p');
  p.innerHTML = text;
  a.appendChild(p);
  nav.appendChild(li);
}
// HERE HARRISON

async function getBusinessName(name) {
  const request = {
    placeId: name,
    fields: ['name', 'formatted_address'],
  };

  const service = new google.maps.places.PlacesService(document.createElement('div'));

  await service.getDetails(request, (place, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      console.log(place.formatted_address);
      console.log(place.name);
      return place.name;
    }
    return 'ero';
  });
}

/*
    Returns an array of the places
*/
async function fetchplaces() {
  const res = await fetch('api/fetchplaces', {
    method: 'get',

  });
  const estimation = await res.json();
  // estimation = estimation.json()
  return estimation;
}

const getPlaceNames = async (arrayOfPlaces) => {
  const result = await arrayOfPlaces.reduce(async (a, place) => {
    // Wait for the previous item to finish processing
    await a;
    await getBusinessName(place);
  }, Promise.resolve());
  return result;
};

const populateSideBarWithPlacesToClick = async () => {
// This is verbose incase we have to come back in 3 years and fix this again

  navigator.geolocation.getCurrentPosition(async () => {
    const placesFetched = await fetchplaces();
    const placesWithNames = await getPlaceNames(placesFetched);
    placesWithNames.forEach((placesWithNames) => addtosidesidebar(placesWithNames, '/', true));
  }, () => {
    addtosidesidebarerror('Location Access Denied', true);
    addtosidesidebarerror('No Locations can be found', true);
  });

  // Function Should get the list of places
  // Function Should get the names of each of the places
  // Function should then add these to the side bar as objects
  // Each of these objects should contain a href to their specific page -
  // I cannot remember what the thought logic was behind this at the present
  // so this will be root for now
};
/// Promise.then(estimation => estimation.data);
/*     navigator.geolocation.getCurrentPosition(
        async function(position) {
            for(var i =0;i<estimation.length;i++){

                var returnedname = await getBusinessName(estimation[i]);

                addtosidesidebar(returnedname, "/", true);
                console.log(returnedname);
                break;
            }
            /* addtosidesidebar("Place 2", "/", false);
            addtosidesidebar("Place 3", "/", true);
            addtosidesidebar("Place 4", "/", false);
            addtosidesidebar("Place 5", "/", false);
            addtosidesidebar("Place 6", "/", false);
            addtosidesidebar("Place 7", "/", true);
            addtosidesidebar("Place 8", "/", true);
            addtosidesidebar("Place 9", "/", false);
            addtosidesidebar("Place 10", "/", false);
           // return estimation;

       // }.bind(this),
        function(error) {
            console.log("[!] Location access allowed")
            addtosidesidebarerror("Location Access Denied", true);
            addtosidesidebarerror("No Locations can be found", true);
       // });

   // return estimation; */
// }
