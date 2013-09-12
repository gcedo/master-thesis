$("#xaxis").change(function() {
  change_x_axis($("#xaxis option:selected").attr("value"));
});

$("#yaxis").change(function() {
  change_y_axis($("#yaxis option:selected").attr("value"));
});

var colors = d3.scale.category20().range();
var palette = {};
var cluster_ids = Array();
var vis = d3.select("#clusters-vis"),
  width = 400,
  height = 400,
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
        $("." + id).hover(
          function() {
            $("." + id).attr("stroke", "red");
          },
          function() {
            $("." + id).attr("stroke", "none");
          })
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

  init();