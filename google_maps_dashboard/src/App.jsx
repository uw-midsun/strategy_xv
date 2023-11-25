import React, { useEffect, useState } from 'react';

function MapComponent() {
  const [path, setPath] = useState(null);

  useEffect(() => {
    function initMap() {
      const map = new window.google.maps.Map(document.getElementById("map"), {
        center: { lat: 40.8829378816515, lng: -98.37406855532743 },
        zoom: 12,
        mapTypeId: "roadmap",
      });

      // Fetch the CSV file
      fetch('sample_race.csv')
        .then((response) => response.text())
        .then((data) => {
          // Parse the CSV data
          var pathCoordinates = [];
          var lines = data.split('\n');
          for (var i = 1; i < lines.length; i++) {
            // Start from 1 to skip the header row
            var parts = lines[i].split(',');
            var id = parseInt(parts[0]);
            var lat = parseFloat(parts[2]);
            var lon = parseFloat(parts[3]);
            // console.log(lat, " + ", lon);
            if (!isNaN(lat) && !isNaN(lon)) {
              pathCoordinates.push(new window.google.maps.LatLng(lat, lon));
            }
          }

          // Create a polyline
          var polyline = new window.google.maps.Polyline({
            path: pathCoordinates,
            geodesic: true,
            strokeColor: '#0096FF',
            strokeOpacity: 1.0,
            strokeWeight: 5,
          });

          // Set the path on the map
          polyline.setMap(map);
          setPath(polyline); // Store the polyline in state
        });
    }

    // Check if the Google Maps API has been loaded
    if (window.google && window.google.maps) {
      initMap();
    } else {
      // You can handle the case where the API hasn't loaded yet
      console.log('Google Maps API is not loaded.');
    }
  }, []);

  const handleRemoveFirst10 = () => {
    if (path) {
      // Get the current path
      const currentPath = path.getPath().getArray();

      // Remove the first 10 elements
      const newPath = currentPath.slice(10);

      // Set the new path on the polyline
      path.setPath(newPath);
    }
  };

  return (
    <div>
      <div id="map" style={{ height: '600px', width: '100%' }}></div>
      <button onClick={handleRemoveFirst10}>Remove First 10 Elements</button>
    </div>
  );
}

export default MapComponent;
