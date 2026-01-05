from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime

with DAG(
    'trigger_external_microservice',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    # Triggering a service in 'target-namespace' from 'airflow-namespace'
    trigger_job = SimpleHttpOperator(
        task_id='trigger_job',
        http_conn_id='sc_api_connection', # Define this in Airflow Connections
        endpoint='api/v1/run-job',           # The route on your microservice
        method='POST',
        data='{"action": "start", "job_id": "123"}',
        headers={"Content-Type": "application/json"},
        # Internal K8s DNS allows cross-namespace communication
        # URL: http://service-name.target-namespace.svc.cluster.local
    )