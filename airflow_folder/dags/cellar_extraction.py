from datetime import datetime, timedelta
import sys
sys.path.append('data_extraction/caselaw/cellar')
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from os.path import dirname, abspath
sys.path.append (dirname(dirname(abspath(__file__))))
from data_extraction.caselaw.cellar.cellar_extraction import download_locally
default_args = {
    'owner': 'none',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='cellar_extraction',
    default_args = default_args,
    description =' Still in process',
    start_date=datetime(2022,7,20),
    schedule_interval='@weekly'

) as DAG:
    task1 = PythonOperator(
        task_id='cellar_transformation',
        python_callable=download_locally
    )