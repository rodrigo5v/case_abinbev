from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'owner': 'Admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['rodrigo.svieira@outlook.com.br'],
}

dag = DAG(
    'breweries',
    default_args=default_args,
    description='Orquestration responsable to Extract , Transform and Load data from API',
    schedule_interval='0 18 * * *',
)

bronze_task = BashOperator(
    task_id='bronze_layer',
    bash_command='python /home/rods/airflow_venv/pipelines/01.bronze/ingestion_breweries.py',
    dag=dag,
)

silver_task = BashOperator(
    task_id='silver_layer',
    bash_command='python /home/rods/airflow_venv/pipelines/02.silver/transform_breweries.py',
    dag=dag,
)

gold_task = BashOperator(
    task_id='gold_layer',
    bash_command='python /home/rods/airflow_venv/pipelines/03.gold/analytics_breweries.py',
    dag=dag,
)

bronze_task >> silver_task >> gold_task