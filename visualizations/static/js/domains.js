$(function() {

  var SLIDER_MIN = 0, SLIDER_MAX = 40135;
  var sliderMin = SLIDER_MIN, sliderMax = SLIDER_MAX;
  var fromDate = new Date(2012,11,30);
  var toDate = new Date();
  var skip = 1;
  var isLoading = false;

  $("#domains-list tr").click(function() {
    window.location.href = $(this).attr("href");
  });

  // Slider
  $("#queries-max").html(SLIDER_MAX);
  $("#queries-min").html(SLIDER_MIN);
	$( "#slider-range" ).slider({
      range: true,
      min: SLIDER_MIN,
      max: SLIDER_MAX,
      values: [ SLIDER_MIN, SLIDER_MAX ],
      slide: function( event, ui ) {
        sliderMin = ui.values[0];
        sliderMax = ui.values[1];
        $("#queries-max").html(ui.values[1]);
        $("#queries-min").html(ui.values[0]);
      }
  });


  // Datepicker
  $( "#datepicker-from" ).datepicker({ onClose: function(selectedDate) { fromDate = selectedDate; } });
  $( "#datepicker-from" ).datepicker("setDate", fromDate);
  fromDate = buildDateString(fromDate);
  $( "#datepicker-to" ).datepicker({ onClose: function(selectedDate) { toDate = selectedDate; } });
  $( "#datepicker-to" ).datepicker("setDate", toDate);
  toDate = buildDateString(toDate);

  // Update page
  $("#update-button").click(function() {

    var url = buildUrl("json");

    $('#myModal').modal('show');
    $.getJSON(url, function(d) {
      r = buildTableHTML(d["data"]);
      $("#domains-list").html(r);
      $('#myModal').modal('hide');
    });
  });

  function buildTableHTML(data) {
    var r = [], j = -1;

      $.each(data, function(index, element) {
        r[++j] = '<tr><td>';
        r[++j] = '<span class="glyphicon glyphicon-globe"></span> ';
        r[++j] = element["domain"];
        r[++j] = '</td><td>';
        r[++j] = '<span class="glyphicon glyphicon-calendar"></span> ';
        r[++j] = dateFormat(new Date(element["first_req_timestamp"]), "ddd, d mmm yyyy");
        r[++j] = '</td><td>';
        r[++j] = '<span class="glyphicon glyphicon-calendar"></span> ';
        r[++j] = dateFormat(new Date(element["last_req_timestamp"]), "ddd, d mmm yyyy");
        r[++j] = '</td><td>';
        r[++j] = '<span class="glyphicon glyphicon-tags"></span> ';
        $.each(element["labels"], function(index, label){
          r[++j] = '<span class="label label-default">' + label + '</span> ';
        });
        r[++j] = '</td></tr>';
      });

      return r.join('');
  }

  // JSON download
  $("#json-download-button").click(function() {
    var url = buildUrl("json");
    window.location.href = url;
  });

  // CSV
  $("#csv-download-button").click(function() {
    var url = buildUrl("csv");
    window.location.href = url;
  });

  function buildUrl(mime) {
    var dga      = "&dga="     + $("#dgaCheckbox").is(':checked');
    var nonDga   = "&nonDga="  + $("#nonDgaCheckbox").is(':checked');
    var nx       = "&nx="      + $("#nxdomainCheckbox").is(':checked');
    var minReqs  = "&minReqs=" + sliderMin;
    var maxReqs  = "&maxReqs=" + sliderMax;
    var since    = "&since="   + fromDate;
    var to       = "&to="      + toDate;

    var url = "/domains?" + mime + dga + nonDga + nx + minReqs + maxReqs + since + to;
    return url;
  }

  function buildDateString(date) {
    return (1 + date.getMonth()) + "/" + date.getDate() + "/" + date.getFullYear();
  }

  function loadMoreDomains() {
    var url = buildUrl("json") + "&skip=" + skip;
    skip++;
    var tableHTML;
    $('#myModal').modal('show');
    $.getJSON(url, function(d) {
      isLoading = true;
      tableHTML = buildTableHTML(d["data"]);
      $("#domains-table > tbody:last").append(tableHTML);
      isLoading = false;
      $('#myModal').modal('hide');
    });
  }

  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() > $(".container").height() - 20 && !isLoading) {
      loadMoreDomains();
    }
  });

});