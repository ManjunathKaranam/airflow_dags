from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'hello_world_dag_dup',
    default_args=default_args,
    description='A simple Hello World DAG',
    schedule=timedelta(days=1),  # Replaced schedule_interval with schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    # Task 1: Print the date
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    # Task 2: Sleep for 5 seconds
    t2 = BashOperator(
        task_id='sleep',
        bash_command='sleep 5',
    )

    # Task 3: Echo hello
    t3 = BashOperator(
        task_id='echo_hello',
        bash_command='echo "Hello World from Kubernetes!"',
    )

    # Define task dependencies
    t1 >> t2 >> t3
