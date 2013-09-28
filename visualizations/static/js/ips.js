$(function() {

  var countries = [];
  var as = [];


  // Checkboxes
  $(".country-checkbox").change(function() {
    var temp = $(".country-checkbox").filter(":checked");
    countries = [];
    $.each(temp, function(index, country) {
      countries.push($(country).attr("id"));
    });
    console.log(countries);
  });

  $(".as-checkbox").change(function() {
    var temp = $(".as-checkbox").filter(":checked");
    as = [];
    $.each(temp, function(index, as_name) {
      as.push($(as_name).attr("id"));
    });
    console.log(as);
  });


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