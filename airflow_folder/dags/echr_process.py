from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'none',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='echr_process',
    default_args = default_args,
    description =' Still in process',
    start_date=datetime(2022,7,20),
    schedule_interval='@daily'

) as DAG:
    task1 =