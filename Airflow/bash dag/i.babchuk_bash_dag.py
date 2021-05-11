from airflow.models import DAG
#from airflow.operators import PythonOperator
from airflow.operators import BashOperator
from datetime import datetime

command = "python /var/lib/airflow/dags/i.babchuk/bash_dag_func.py"

default_args = {
    'owner': 'i-babchuk',
    'depends_on_past': False,
    'retries': 0
}


dag = DAG('Bash_report_sender_i.babchuk', 
          default_args=default_args,
          schedule_interval='0 12 * * 1',
          start_date = datetime(2021, 2, 12))



task = BashOperator(task_id='send_report_to_VK', 
                    bash_command=command,
                    dag=dag)


