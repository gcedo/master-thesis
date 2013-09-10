$(function() {
  var map;

  function initialize() {
    var mapOptions = { 
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      center: new google.maps.LatLng(-34.397, 150.644),
      zoom: 2
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
  }

  function getDomainJson(domain) {
    var items = [];
    $.getJSON('/domain/' + domain + '?json', function(data){
      $.each(data, function(key, val) {
        for (ip in data.ips) {
          items.push({"lat": data.ips[ip].latitude, "lon": data.ips[ip].longitude});
        }
      });
      addMarkers(items);
    });

  }

  function addMarkers(items) {
    console.log(items)
    $.each(items, function(k, item) {
      console.log(item)
      var loc = new google.maps.LatLng(parseFloat(item.lat), parseFloat(item.lon));
      
      addMarker(loc);
    })
  }

  function addMarker(loc) {
    marker = new google.maps.Marker({
      position: loc,
      map: map
    });
  }

  initialize();
  getDomainJson('sophosxl.com');
});