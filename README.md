# Pedview

## Inspiration
Edmonton's winters can be extremely harsh, with temperatures plummeting to nearly -30°C. In such conditions, spending time outdoors can be uncomfortable and even hazardous. This challenge inspired us to develop a solution: a map that guides users to their classes by utilizing a combination of pedways and main roads. Our goal is to minimize the time spent outside, helping users stay warm and safe during the winter months.

## What It Does
Our solution provides users with the most efficient route to their classes by combining pedways and main roads. This approach ensures that users spend the least amount of time exposed to the cold, prioritizing their comfort and well-being.

## How We Built It
The project was developed using Flask for the backend, with HTML and CSS forming the frontend. We also integrated several APIs to facilitate access to the necessary map data, enabling us to create a functional and user-friendly application.

## Challenges We Encountered
One of the significant challenges we faced was refining our Python model to accurately determine the shortest route. The model initially struggled to distinguish between main streets and pedways, complicating the routing process.

## Accomplishments We’re Proud Of
We take pride in our ability to collaborate effectively as a team to develop a practical solution that serves not only our needs but also those of the broader University of Alberta student community.

## What's Next for Pedview
Looking ahead, we plan to expand our project by developing a mobile application and incorporating a street view feature. These enhancements will further improve the user experience and accessibility of our solution.

## Built With
- CSS
- Flask
- HTML
- JavaScript
- Python

## Installation

1. **Set up the Backend:**
   ```bash
   cd backend_files
   source new_env/bin/activate
   pip install -r requirements.txt 
   python3 app.py

2.**Set up the Frontend:**
  ```bash
  cd ..
  npm run dev


