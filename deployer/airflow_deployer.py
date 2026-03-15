import pickle
from airflow.sdk import DAG
from deployer.deployer import Deployer
import os
import shutil
import subprocess
import logging

logger = logging.getLogger(__name__)


class AirflowDeployer(Deployer):

    def __init__(self, dag_file_path: str, repo_url: str, dags_dir: str = "/opt/airflow/dags"):
        """
        The '__init__()' function gets a dag file path, a remote repo URL, and a local dags directory
        and initializes the AirflowDeployer.
        """
        self.dag_file_path = dag_file_path
        self.repo_url = repo_url
        self.dags_dir = dags_dir

    def _git_sync(self) -> bool:
        """
        The '_git_sync()' function syncs the local dags directory with the remote git repository
        clones it if it doesn't exist, else it pulls the latest changes, and returns True on success.
        """
        try:
            if not os.path.exists(self.dags_dir):
                subprocess.run(["git", "clone", self.repo_url, self.dags_dir], check=True)
                logger.info(f"Cloned repo into {self.dags_dir}")
            else:
                subprocess.run(["git", "-C", self.dags_dir, "pull"], check=True)
                logger.info("Git pull completed.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Git sync failed: {e}")
            return False

    def push_dag_to_git(self, dag_file_path: str) -> bool:
        """
        The 'push_dag_to_git()' function gets a filepath of a DAG file, copies it into
        the local repo directory, and pushes it to the remote git repository.
        """
        try:
            dag_name = os.path.basename(dag_file_path)
            dest = os.path.join(self.dags_dir, dag_name)
            shutil.copy2(dag_file_path, dest)

            subprocess.run(["git", "-C", self.dags_dir, "add", dag_name], check=True)
            subprocess.run(["git", "-C", self.dags_dir, "commit", "-m", f"Add DAG: {dag_name}"], check=True)
            subprocess.run(["git", "-C", self.dags_dir, "push"], check=True)

            logger.info(f"DAG '{dag_name}' pushed to git successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Git push failed: {e}")
            return False

    def deploy(self) -> bool:
        """
        The 'deploy()' function syncs the created_dags directory with git and copies the dag file into it,
        so that Airflow's Executor can detect and run it.
        """

        dag_file_path = self.create_dag_file()

        if not self.push_dag_to_git(dag_file_path):
            return False

        if not self._git_sync():
            return False

        logger.info(f"DAG '{os.path.basename(dag_file_path)}' deployed successfully.")
        return True