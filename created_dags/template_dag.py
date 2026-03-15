import os
import pickle
from airflow.sdk import DAG

path = os.path.abspath("pickles")

def load_dag():
    curr_path = os.path.relpath(__file__)
    file_name = curr_path.split("/")[-1]
    file_name = file_name.replace(".py", ".pickle")
    pickle_path = f"{path}/{file_name}"
    with open(pickle_path, "rb") as file:
        created_dag = pickle.load(file)
    return created_dag
