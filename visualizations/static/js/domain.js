function loadVisualizations(dataset_url) {

  // Fetch JSON data and pass it to the visualizations.
  d3.json(dataset_url, function(error, dataset) {
    drawIPNetwork(dataset);
    drawTimeline(dataset);
    loadMarkers(dataset);
  });
}