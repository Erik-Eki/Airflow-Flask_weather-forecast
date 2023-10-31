from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import smtplib
from email.mime.text import MIMEText
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 31),
    'email': ['eriko.oy38@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'weather_report', default_args=default_args, schedule_interval=timedelta(days=1))

def fetch_weather():
    response = requests.get('http://flask-app:80/weather')
    return response.json()

def email_weather(**context):
    task_instance = context['task_instance']
    weather = task_instance.xcom_pull(task_ids='fetch_weather')

    # Email the weather data (this is just a placeholder)
    print(f"Emailing weather: {weather}")
    # Create a text/plain message
    msg = MIMEText(f"Here's today's weather: {weather}")

    email = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Weather from Airflow DAG event'
    msg['From'] = email
    msg['To'] = email
    # Send the message via Gmail's SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, password)
    s.sendmail(email, [email], msg.as_string())
    s.quit()

fetch_weather = PythonOperator(
    task_id='fetch_weather',
    python_callable=fetch_weather,
    dag=dag)

email_weather = PythonOperator(
    task_id='email_weather',
    python_callable=email_weather,
    provide_context=True,
    dag=dag)

fetch_weather >> email_weather
