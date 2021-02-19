from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from Data_Pull import get_events
from datetime import date, timedelta, datetime
from gdelt import gdelt as gdelt_client
from airflow.operators.postgres_operator import PostgresOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    'wait_for_downstream': False,
    "start_date": datetime(2021, 2, 3), # we start at this date to be consistent with the dataset we have and airflow will catchup
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}


dag = DAG('GDELT', default_args= default_args, schedule_interval= None)

unload_data ='./scripts/unload_data.sql'
def success():
     print('success')

with dag:
    collect_task = PythonOperator(
         dag=dag,
         task_id = 'collect_GDELT_data',
         python_callable= get_events,
         provide_context=False,
         op_kwargs={'country_code' : 'MO', 'start_date' : date.today() , 'max_days' : 10}        
    )
    end_task = PythonOperator(
         dag=dag,
         task_id='End',
         python_callable=success,
         provide_context=False,
    )
    pg_unload = PostgresOperator(
         dag=dag,
         task_id='pg_unlaod',
         sql = unload_data,
         postgres_conn_id='postgres_default',
         depends_on_past=True,
         wait_for_downstream=True,
    )

    collect_task >> pg_unload >> end_task