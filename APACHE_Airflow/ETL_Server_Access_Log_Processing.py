# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Rodrigo Azevedo',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'server access',
    default_args=default_args,
    description='server access',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task

download = BashOperator(
    task_id='download',
    bash_command='wget -O /home/project/airflow/dags/server-access-log.txt "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"',
    dag=dag,
)

# define the second task
extract = BashOperator(
    task_id='extract_timestamp_visitorid',
    #bash_command="awk -F '#' '{print $1, $4}' server-access-log.txt > extracted-fields.txt",
    bash_command="cut -d '#' -f 1,4 /home/project/airflow/dags/server-access-log.txt > /home/project/airflow/dags/extracted-fields.txt",
    dag=dag,
)

# define the third task
transform = BashOperator(
    task_id='capitalize_visitorid',
    bash_command="cut -d '#' -f 2 extracted-fields.txt | tr '[a-z]' '[A-Z]' < /home/project/airflow/dags/extracted-fields.txt  > /home/project/airflow/dags/transformed-fields.txt",
    dag=dag,
)

# define the forth task
transform = BashOperator(
    task_id='compress',
    bash_command="zip log.zip transformed-fields.txt",
    dag=dag,
)
# task pipeline
download >> extract_timestamp_visitorid >> capitalize_visitorid >> compress