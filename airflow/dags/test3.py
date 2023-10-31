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
    'flask_request', default_args=default_args, schedule_interval=timedelta(days=1))

def make_request_to_flask():
    response = requests.get('http://flask-app:80/dag-test')
    # Do something with 'response'
    return response.json()

def process_response(**context):
    task_instance = context['task_instance']
    response = task_instance.xcom_pull(task_ids='make_request')
    # Process the response here
    print(f"Response from Flask app: {response['message']}")

make_request = PythonOperator(
    task_id='make_request',
    python_callable=make_request_to_flask,
    dag=dag)

process_response = PythonOperator(
    task_id='process_response',
    python_callable=process_response,
    provide_context=True,
    dag=dag)

make_request >> process_response
