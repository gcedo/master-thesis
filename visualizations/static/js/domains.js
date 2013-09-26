$(function() {

  var SLIDER_MIN = 0, SLIDER_MAX = 3585;
  var sliderMin = 0, sliderMax = 0;
	// Slider
	$( "#slider-range" ).slider({
      range: true,
      min: SLIDER_MIN,
      max: SLIDER_MAX,
      values: [ SLIDER_MIN, SLIDER_MAX ],
      slide: function( event, ui ) {
        sliderMin = ui.values[0];
        sliderMax = ui.values[1];
      }
  });

  $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
    " - $" + $( "#slider-range" ).slider( "values", 1 ) );

  // Datepicker
  $( "#datepicker-from" ).datepicker();
  $( "#datepicker-to" ).datepicker();

  // Update page
  $("#update-button").click(function() {
    var dga     = "&dga="    + $("#dgaCheckbox").is(':checked');
    var nonDga  = "&nonDga=" + $("#nonDgaCheckbox").is(':checked');
    var nx      = "&nx="     + $("#nxdomainCheckbox").is(':checked');
    var minReqs = "&minReqs=" + sliderMin;
    var maxReqs = "&maxReqs=" + sliderMax;

    var url = "/domains?json" + dga + nonDga + nx + minReqs + maxReqs;

    alert(url);

    $.getJSON(url, function(d) {
      var r = new Array(), j = -1;

      $.each(d["data"], function(index, element) {
        r[++j] = '<tr><td>';
        r[++j] = element["domain"];
        r[++j] = '</td><td>';
        r[++j] = element["first_req_timestamp"];
        r[++j] = '</td><td>';
        r[++j] = element["last_req_timestamp"];
        r[++j] = '</td><td>';
        r[++j] = element["labels"];
        r[++j] = '</td></tr>';
      });

      $("#domains-list").html(r.join(''));

    });
  });
});