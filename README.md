# Airflow + Flask Weather-forecast

This small app has a Flask server and Airflow running in Docker containers in the same network. Done for learning purposes.

Flask server does a GET request to https://www.weatherapi.com to get current weather in Kajaani.

In Airflow, there's a task that fetches that weather data from the API endpoint and emails the weather data to an email address (configures in environment variables)
