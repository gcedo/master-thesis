$("#xaxis").change(function() {
  change_x_axis($("#xaxis option:selected").attr("value"));
});

$("#yaxis").change(function() {
  change_y_axis($("#yaxis option:selected").attr("value"));
});

$("#select-cluster").change(function() {
  $("svg circle").attr("stroke", "none");
  if ($("#select-cluster option:selected").attr("value") == "none") { return; }
  highlight_cluster($("#select-cluster option:selected").attr("value"));
  load_cluster_info($("#select-cluster option:selected").attr("value"))
})

var colors = d3.scale.category20().range();
var palette = {};
var cluster_ids = Array();
var vis = d3.select("#clusters-vis"),
  width = 500,
  height = 500,
  margins = {top: 20, right: 20, bottom: 20, left: 30},
  xMin = 0,
  xMax = 300,
  yMin = 0,
  yMax = 300,
  xRange = d3.scale.linear()
             .range([margins.left, width - margins.right]).domain([xMin, xMax]),
  yRange = d3.scale.linear()
             .range([height - margins.top, margins.bottom]).domain([yMin, yMax]),
  xAxis = d3.svg.axis()
            .scale(xRange)
            .tickSize(5),
  yAxis = d3.svg.axis()
            .scale(yRange)
            .tickSize(5)
            .orient("left"),
  circles;

function init() {
  d3.json("/static/data/clusters.json", function(error, json) {
    vis.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + (height - margins.bottom) + ")")
      .call(xAxis);

    vis.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + (margins.left) + ",0)")
      .call(yAxis)

    $.each(json.domains, function(index, domain) {
      if (cluster_ids.indexOf(domain.cluster) == -1) {
        cluster_ids.push(domain.cluster);
      }
    });

    $.each(cluster_ids, function(index, element) {
      palette[element] = colors[index];
    });

    update(json.domains);

    $.each(cluster_ids, function(index, id) {
      $('#select-cluster')
         .append($("<option></option>")
         .attr("value", id)
         .text(id)); 

      $("." + id).hover(
        function() { $("." + id).attr("stroke", "red");  },
        function() { $("." + id).attr("stroke", "none"); }
        );
      $("." + id).click(
        function() {
          highlight_cluster(id);
          load_cluster_info(id);
        }
      );
    });
  });
}

function update(data) {
  circles = vis.selectAll("circle")
                 .data(data, function(d) { return d.url; });
  circles.enter()
    .insert("circle")
      .attr("cx", function(d) { return xRange(+d.cf1); })
      .attr("cy", function(d) { return yRange(+d.cf2); })
      .attr("class", function(d) { return d.cluster; })
      .attr("r", 2)
      .style("fill", function(d) { return palette[d.cluster]; });
}

function change_x_axis(domain) {
  circles.transition().duration(1000).ease("exp-in-out")
    .attr("cx", function(d) { return xRange(+d[domain])});
}

function change_y_axis(domain) {
  circles.transition().duration(1000).ease("exp-in-out")
    .attr("cy", function(d) { return yRange(+d[domain])});
}

function highlight_cluster(cluster) {
  $("." + cluster).attr("stroke", "red");
}

function load_cluster_info(cluster) {
  $.getJSON('/static/data/p_entropy_test.json', function(data){
    $.each(data.clusters, function(index, element) {
      if (element.ID == cluster) {
        $("#cluster-size").html(element.size);
        $("#cluster-mapping").html(element.ip_mapping_size);
        $("#cluster-length").html(element.length);
        $("#cluster-char-length").html(element.char_set_len);
        $("#cluster-num-ratio").html(element.numerical_characters_ratio);
        $("#cluster-mean-ratio").html(element.meaningful_word_ratio);
        $("#cluster-one-gram").html(element.one_gram_normality_score);
        $("#cluster-two-gram").html(element.two_gram_normality_score);
        $("#cluster-three-gram").html(element.three_gram_normality_score);
      }
    })
  });
}

init();