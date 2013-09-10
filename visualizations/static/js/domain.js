function get_domain_json(domain) {
  $.getJSON('/domain/' + domain + '?json', function(data){
    var items = [];

    $.each(data, function(key, val) {
      console.log('key: ' + key + ', val: ' + val)
    });
  });
}