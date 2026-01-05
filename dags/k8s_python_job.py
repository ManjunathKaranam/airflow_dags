from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'k8s_python_job',
    default_args=default_args,
    description='A DAG to run a Python job in a Kubernetes Pod',
    schedule_interval=None,
    catchup=False,
) as dag:

    run_python_job = KubernetesPodOperator(
        task_id='run_python_job',
        name='python-job-pod',
        namespace='airflow',
        image='python:3.9-slim',
        cmds=["python", "-c"],
        arguments=["print('Hello from Kubernetes Pod!')"],
        labels={"app": "python-job"},
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
    )
