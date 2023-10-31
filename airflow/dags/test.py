from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

# Define the function that sends a POST request to the Flask app
def predict_value():
    url = 'http://flask-app:5555/predict'
    data = {'features': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]}
    response = requests.post(url, json=data, headers = {'Content-Type': 'application/json'})
    prediction = response.json()['prediction']
    print(f'Predicted Value: {prediction}')

def send_dag():
    dag_data = {"message": "Hello from Airflow!", "data": [1,2,3,4,5]}  # Replace with your actual DAG data
    response = requests.post('http://flask-app:5555/predict', json=dag_data, headers = {'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise Exception('Failed to send DAG')
    
# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 15),
    'retries': 1,
}

# Create the DAG object
dag = DAG(
    dag_id='1_TEST-predict_value_dag',
    default_args=default_args,
    schedule_interval='@daily',
)

# Create the task that runs the predict_value function
predict_value_task = PythonOperator(
    task_id='1_TEST-predict_value_dag',
    python_callable=predict_value,
    dag=dag,
)


dag2 = DAG(
    dag_id='2_TEST',
    default_args=default_args,
    schedule_interval='@daily',
)
test_2_dag_task = PythonOperator(
    task_id='2_TEST',
    python_callable=send_dag,
    dag=dag2
)

# Set the task dependencies (none in this case)
predict_value_task
test_2_dag_task
