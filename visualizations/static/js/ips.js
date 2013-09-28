$(function() {

// JSON download
  $("#json-download-button").click(function() {
    var url = buildUrl("json");
    window.location.href = url;
  });

  function buildUrl(mime) {
    var url = "/ips?" + mime;
    return url;
  }

});