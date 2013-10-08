var map;

function initialize() {
  var mapOptions = {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: new google.maps.LatLng(31.802893, 9.316466),
    zoom: 1
  };
  map = new google.maps.Map(document.getElementById("map-canvas-domain"), mapOptions);
}

function loadMarkers(dataset) {
  var items = [];
  for (var ip in dataset.ips) {
    items.push({"lat": dataset.ips[ip].latitude, "lon": dataset.ips[ip].longitude});
  }
  addMarkers(items);
}

function addMarkers(items) {
  $.each(items, function(k, item) {
    var loc = new google.maps.LatLng(parseFloat(item.lat), parseFloat(item.lon));
    addMarker(loc);
  });
}

function addMarker(loc) {
  marker = new google.maps.Marker({
    position: loc,
    map: map
  });
}

initialize();