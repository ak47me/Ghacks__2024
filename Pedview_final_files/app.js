
let map;
let directionsService;
let directionsRenderer1;
let directionsRenderer2;
let pathPolyline;

// Initialize and display the map
function initMap() {
const center = { lat: 53.5250, lng: -113.5212 };
map = new google.maps.Map(document.getElementById('map'), {
  zoom: 16,  // Default zoom level
  center: center
});

directionsService = new google.maps.DirectionsService();
directionsRenderer1 = new google.maps.DirectionsRenderer({ map: map, preserveViewport: true });
directionsRenderer2 = new google.maps.DirectionsRenderer({ map: map, preserveViewport: true });


const submitButton = document.getElementById("submit");
submitButton.addEventListener("click", () => {
document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'start' })
  const start = document.getElementById("from").value;
  const end = document.getElementById("to").value;
  console.log(start, end);
  // Send POST request to Flask Python site
  fetch("http://127.0.0.1:5000/api/coordinates", { // Update URL to match Flask endpoint
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ start, end })
  })
  .then(response => {
    console.log(response);
    return response.json();
})

  .then(data => {
      // After receiving the response, start fetching the start, end, and path data
      return fetch('http://127.0.0.1:5000/api/coordinates/start')
  })
  .then(response => response.json())
  .then(data => {
      const start = new google.maps.LatLng(data.start[0], data.start[1]);
      const end = new google.maps.LatLng(data.end[0], data.end[1]);
      calculateAndDisplayRoute(start, end, directionsRenderer1);

      // Fetch end coordinates after start is fetched
      return fetch('http://127.0.0.1:5000/api/coordinates/end');
  })
  .then(response => response.json())
  .then(data => {
      const start = new google.maps.LatLng(data.start[0], data.start[1]);
      const end = new google.maps.LatLng(data.end[0], data.end[1]);
      calculateAndDisplayRoute(start, end, directionsRenderer2);

      // Fetch the path after end coordinates are fetched
      return fetch('http://127.0.0.1:5000/api/path');
  })
  .then(response => response.json())
  .then(data => {
      const pathCoordinates = data.path.map(coord => ({
          lat: coord[0],
          lng: coord[1]
      }));
      drawPath(pathCoordinates);
  })
  .catch(error => {
      console.error('Error:', error);
  });
});
}

// Function to calculate and display the shortest route
function calculateAndDisplayRoute(start, end, directionsRenderer) {
const request = {
  origin: start,
  destination: end,
  travelMode: google.maps.TravelMode.WALKING
};

directionsService.route(request, (response, status) => {
  if (status === google.maps.DirectionsStatus.OK) {
      directionsRenderer.setDirections(response);
  } else {
      alert('Directions request failed due to ' + status);
  }
});
}

// Function to draw the path on the map
function drawPath(pathCoordinates) {
if (pathPolyline) {
  pathPolyline.setMap(null); // Remove previous path if any
}

pathPolyline = new google.maps.Polyline({
  path: pathCoordinates,
  geodesic: true,
  strokeColor: '#FF0000',
  strokeOpacity: 1.0,
  strokeWeight: 2
});
pathPolyline.setMap(map);
}



window.onload = function() {
    setTimeout(() => {
      document.querySelector('.logo-left').classList.add('split-left');
      document.querySelector('.logo-right').classList.add('split-right');

      setTimeout(() => {
        const logoContainer = document.querySelector('.logo-container');
        logoContainer.classList.add('fade-out');

        setTimeout(() => {
          logoContainer.style.display = 'none';
          document.querySelector('.homepage-content').classList.add('show');
          document.querySelector('.search').classList.add('show');
          document.querySelector('.map').classList.add('show');
        }, 1000); // Match this with the fade-out duration
      }, 2000); // This should match the logo split transition duration
    }, 1000); // Initial delay before the logo split animation starts
    initMap();
  };

