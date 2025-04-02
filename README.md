# Mission Impossible - CRUD Application

This project involves building a CRUD (Create, Read, Update, Delete) application to manage resource stocks in a space station. The application uses Flask for the backend, SQLite for the database, and provides a simple HTML/JS user interface.

## Technical Stack

| Component     | Technology         |
|---------------|--------------------|
| Backend       | Flask              |
| Database      | SQLite             |
| Frontend      | HTML/JS            |
| Infrastructure| Docker             |
| CI/CD         | GitHub Actions     |

## Quick Start

### Prerequisites
To run this project locally, you will need the following:

- Docker 20.10+
- Python 3.10+  

### Local Development

Follow these steps to get the application up and running locally:

```bash
# 1. Clone the repository
git clone https://github.com/pelagiavlas/missionImpossible
cd missionImpossible

# 2. Start with Docker Compose
docker-compose up --build

# Access the endpoints:
# - BACKEND: http://localhost:5000
# - API: http://localhost:5000/products
# - UI: http://localhost:8080


### Run Tests
pip install -r requirements.txt
pytest tests/

### Stop the application
docker-compose down
