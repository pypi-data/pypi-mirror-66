from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

from databricks_api import DatabricksAPI
from requests import HTTPError

from cognite.databricks_utils.file_util import write_list


class JobChecker:
    def __init__(self, location: str, token: str):
        host = f"https://{location}.azuredatabricks.net"
        self.client = DatabricksAPI(host=host, token=token)
        self.job_without_notebook: List[str] = []
        self.job_without_creator: List[str] = []
        self.job_without_new_runs: List[str] = []
        self.job_without_success: List[str] = []

    def get_runs(self, job_id: str) -> Tuple[bool, List[Dict]]:
        runs = self.client.jobs.list_runs(job_id=job_id)
        if "runs" in runs:
            return True, runs["runs"]
        return False, []

    def path_exists(self, path: str) -> bool:
        try:
            self.client.workspace.get_status(path)
            return True
        except HTTPError:
            return False

    def get_creator(self, job: Dict, job_name: str) -> str:
        if "creator_user_name" not in job:
            self.job_without_creator.append(job_name)
            return ""
        else:
            return job["creator_user_name"]

    def check_has_notebook(self, job_settings: Dict, job_name: str, creator: str) -> None:
        if "notebook_task" in job_settings and "notebook_path" in job_settings["notebook_task"]:
            if not self.path_exists(job_settings["notebook_task"]["notebook_path"]):
                self.add_job_string(job_name, creator, self.job_without_notebook)
        else:
            self.add_job_string(job_name, creator, self.job_without_notebook)

    def check_has_recent_runs(self, run: Dict[str, Any], job_name: str, creator: str) -> None:
        if not self.timestamp_within_x_days(run["start_time"], 10):
            self.add_job_string(job_name, creator, self.job_without_new_runs)

    def check_has_recent_success(self, runs: List[Dict[str, str]], job_name: str, creator: str):
        if len(runs) <= 3:
            return
        for run in runs[0 : (10 if len(runs) >= 10 else len(runs))]:  # noqa
            if self.run_is_successful(run):
                return

        self.add_job_string(job_name, creator, self.job_without_success)

    def check_runs(self, runs: List[Dict[str, Any]], job_name: str, creator: str) -> None:
        self.check_has_recent_runs(runs[0], job_name, creator)
        self.check_has_recent_success(runs, job_name, creator)

    def run(self):
        jobs = self.client.jobs.list_jobs()["jobs"]
        counter = 0
        for job in jobs:
            counter += 1
            job_settings = job["settings"]
            job_name = job_settings["name"]
            print(f"Checking job named {job_name} ({counter}/{len(jobs)})")

            creator = self.get_creator(job, job_name)
            self.check_has_notebook(job_settings, job_name, creator)

            has_runs, runs = self.get_runs(job["job_id"])
            if has_runs:
                self.check_runs(runs, job_name, creator)

    def write_results_to_file(self, file_path: str):
        write_list(file_path, "Jobs without notebooks", self.job_without_notebook)
        write_list(file_path, "Jobs without creator", self.job_without_creator)
        write_list(file_path, "Jobs without recent runs (last 10 days)", self.job_without_new_runs)
        write_list(file_path, "Jobs without recent success (last 10 runs)", self.job_without_success)

    @staticmethod
    def run_is_successful(run: Dict[str, Any]) -> bool:
        return (
            "state" in run
            and "life_cycle_state" in run["state"]
            and "result_state" in run["state"]
            and run["state"]["life_cycle_state"] == "TERMINATED"
            and run["state"]["result_state"] == "SUCCESS"
        )

    @staticmethod
    def add_job_string(job_name: str, creator: str, job_list: List[str]) -> None:
        job_list.append(f"{job_name}{f' ({creator})' if creator else ''}")

    @staticmethod
    def timestamp_within_x_days(timestamp: int, x: int) -> bool:
        ten_days_ago = datetime.now() - timedelta(days=x)
        dt = datetime.fromtimestamp(timestamp / 1e3)
        return dt > ten_days_ago
