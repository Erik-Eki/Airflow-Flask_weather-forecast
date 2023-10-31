from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 31),
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'random_thing', default_args=default_args, schedule_interval=timedelta(days=1))

def make_request_to_flask():
    response = requests.get('http://flask-app:5555/dag')
    print(response)
    if response.status_code != 200:
        raise Exception('Failed to send DAG')
    # Do something with 'response'

make_request = PythonOperator(
    task_id='make_request_random_thing',
    python_callable=make_request_to_flask,
    dag=dag)