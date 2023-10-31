# Airflow + Flask Weather-forecast

This small app has a Flask server and Airflow running in Docker containers in the same network. Done for learning purposes.

1. Flask server does a GET request to https://www.weatherapi.com to get current weather in Kajaani.
2. In Airflow, there's a task that fetches that weather data from the API endpoint
3. Airflow emails the weather data to an email address (configures in environment variables)


Improvements:
- Adding Flask server container to be built with the same docker-compose.yaml as Airflow
- Probably a better way of storing email and passwords than .env
