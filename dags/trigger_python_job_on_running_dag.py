from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    'trigger_remote_python_script',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_script_remote = KubernetesPodOperator(
        task_id='execute_remote_python',
        name='airflow-executor-client',
        namespace='airflow',
        image='bitnami/kubectl:latest',
        cmds=["/bin/sh", "-c"],
        arguments=[
            """
            set -e
            # 1. Find a running pod name
            TARGET=$(kubectl get pods -n innovations -l app=pythonapi --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}')
    
            # 2. Find the first container name in that pod
            CONTAINER=$(kubectl get pod "$TARGET" -n innovations -o jsonpath='{.spec.containers[0].name}')
    
            echo "Executing on Pod: $TARGET, Container: $CONTAINER"
    
            # 3. Exec with explicit container name
            kubectl exec -n innovations "$TARGET" -c "$CONTAINER" -- python3 /appt_count.py
            """
        ],
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
    )