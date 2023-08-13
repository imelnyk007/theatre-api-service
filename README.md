# Theatre API Service

Theatre API Service is a API for managing theatre plays, theatre hall, performance, 
and reservation tickets for performance.

# Getting started

## Prerequisites
Make sure you have the following installed:
* Python (version 3.6 or higher)
* Docker

## Installation
There are two ways to set up the project:
* Clone from Git
* Pull from Docker Hub

### Clone from Git:
1. Clone the repository:
```bash
https://github.com/imelnyk007/theatre-api-service.git
```
2. Navigate to the project directory:
```bash
cd theatre-api-service
```
3. Create an .env file and define the environment variables using .env.sample.
4. Build Docker container:
```bash
docker-compose build
```
5. Start the Docker container:
```bash
docker-compose up -d
```
6. If you want to test the project with non-empty database, you can load fixtures:
```bash
docker-compose exec app python manage.py loaddata data.json
```
Use the following credentials to log in as superuser:
```angular2html
Email: admin@admin.com
Password: 1qazcde3
```
Or create another superuser using the following command:
```bash
docker-compose exec app python manage.py createsuperuser
```
7. Don't forget to stop the Docker container when you're done:
```bash
docker-compose down
```

### Pull from Docker Hub:
1. Pull the project:
```bush
docker pull melnyk007/theatre-api-service
```
2. Start the Docker container:
```bash
docker-compose up -d
```
3. If you want to test the project with non-empty database, you can load fixtures:
```bash
docker-compose exec app python manage.py loaddata data.json
```
Use the following credentials to log in as superuser:
```angular2html
Email: admin@admin.com
Password: 1qazcde3
```
Or create another superuser using the following command:
```bash
docker-compose exec app python manage.py createsuperuser
```
4. Don't forget to stop the Docker container when you're done:
```bash
docker-compose down
```

## API Documentation
The API documentation can be accessed at http://localhost:8000/swagger/ which provides an interactive 
interface to explore and test the available API endpoints.

## API Endpoints
```
"theatre" : 
                "http://127.0.0.1:8000/api/theatre/genres/"
                "http://127.0.0.1:8000/api/theatre/actors/"
                "http://127.0.0.1:8000/api/theatre/plays/"
                "http://127.0.0.1:8000/api/theatre/theatre-halls/"
                "http://127.0.0.1:8000/api/theatre/performances/"
                "http://127.0.0.1:8000/api/theatre/reservations/"
"user" : 
                "http://127.0.0.1:8000/api/user/register/"
                "http://127.0.0.1:8000/api/user/me/"
                "http://127.0.0.1:8000/api/user/token/"
                "http://127.0.0.1:8000/api/user/token/refresh/"
"documentation": 
                "http://127.0.0.1:8000/api/doc/"
                "http://127.0.0.1:8000/api/swagger/"
                "http://127.0.0.1:8000/api/redoc/"
```

## DB Structure
![DB_structure_Theatre_API_Service.png](..%2F..%2FDesktop%2FDB_structure_Theatre_API_Service.png)