# Turing Test Tool

This app serves randomized clinical note sections from a MySQL database and allows users to guess if they're synthetic or real. Responses are saved as text files.

## Getting Started

### Prerequisites

- Docker installed
- Docker Desktop running

## Running the App

1. Clone the repo and open the project folder.
2. Make sure Docker is running.
3. Run the app:

   docker-compose up --build

4. Once running, open your browser at:

   http://localhost:5001

## API Endpoints

- GET /generate-section  
  Returns a random clinical note section from the database.

- POST /submit-response  
  Submits the user's guess and reasoning. Saves a text file in `responses/`.

## Response File Location

Response files are saved to /responses

This folder is mounted into the container at /app/responses using Docker volumes.

## Stopping the App

To stop everything and remove containers + database data:

docker-compose down -v

## Troubleshooting

- Port already in use?  
  Change the host port in `docker-compose.yml` (e.g., 3308:3306 or 5003:5000)

- Response file not saving?  
  Make sure the `responses/` folder exists and is correctly mounted.
