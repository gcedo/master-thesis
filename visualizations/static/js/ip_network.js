function drawIPNetwork (dataset) {
  var width = 500,
      height = 300,
      linkDistance = 100,
      charge = -300;

  var svg = d3.select("#graph").append("svg:svg")
              .attr("width", width)
              .attr("height", height);

  var force = d3.layout.force()
                .linkDistance(linkDistance)
                .charge(charge)
                .size([width, height]);

  var rect_width = 100,
      rect_height = 20,
      font_size = 15;

  var color = d3.scale.category20();
  var links = [];
  var nodes = [];

  nodes.push({"name" : dataset.domain, "group" : 1 });
  var counter = 0;
  $.each(dataset.ips, function(key, value) {
    nodes.push({"name" : key, "group" : 2 });
    links.push({"source" : 0, "target" : ++counter});
  });

  force
    .nodes(nodes)
    .links(links)
    .start();

  var link = svg.selectAll(".link")
    .data(links)
  .enter().append("svg:line")
    .attr("class", "link")
    .style("stroke-width", "2px")
    .style("stroke", "#ddd");

  var node = svg.selectAll(".node")
    .data(nodes)
  .enter().append("svg:g")
    .attr("class", "node")
  .append("svg:rect")
    .attr("width", rect_width)
    .attr("height", rect_height)
    .attr("rx", "3px")
    .attr("ry", "3px")
    .attr("fill", function(d) { return color(d.group); })
    .call(force.drag);

  var texts = svg.selectAll("text.label")
    .data(nodes)
    .enter().append("text")
    .attr("class", "label")
    .attr("fill", function(d) {
      if (d.group == 1) return "#fff";
      else              return "#000";
    })
    .attr("font-family", "sans-serif")
    .attr("font-size", font_size + "px")
    .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("x", function(d) { return d.x - rect_width / 2; })
        .attr("y", function(d) { return d.y - rect_height / 2; });

    texts.attr("transform", function(d) {
      var bbox = this.getBBox();
      var x_offset = bbox.width / 2;
      var y_offset = bbox.height / 2 - font_size / 4;
      return "translate(" + (d.x - x_offset) + ", " + (d.y + y_offset) + ")";
    });
  });
}