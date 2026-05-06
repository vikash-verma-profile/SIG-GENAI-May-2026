"""
Optional Airflow DAG sketch (requires apache-airflow; not installed by default).

Uncomment and install airflow to use in your Airflow environment.
"""

# from datetime import datetime
#
# import pandas as pd
# from airflow import DAG
# from airflow.operators.python import PythonOperator
#
#
# def ingest():
#     pd.read_csv("data/shipments.csv")
#
#
# def clean():
#     pass
#
#
# def transform():
#     pass
#
#
# def load():
#     pass
#
#
# dag = DAG("logistics_dag", start_date=datetime(2024, 1, 1), schedule_interval="@daily")
# t1 = PythonOperator(task_id="ingest", python_callable=ingest, dag=dag)
# t2 = PythonOperator(task_id="clean", python_callable=clean, dag=dag)
# t3 = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
# t4 = PythonOperator(task_id="load", python_callable=load, dag=dag)
# t1 >> t2 >> t3 >> t4
