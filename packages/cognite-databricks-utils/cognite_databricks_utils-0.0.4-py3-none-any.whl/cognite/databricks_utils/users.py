from enum import Enum
from typing import Callable, Dict, List

import requests
import xlrd


class Action(Enum):
    ADD = "add"
    DELETE = "delete"


class UsersHandler:
    def __init__(self, location: str, token: str, users_file: str):
        self.header = {"Content-Type": "application/scim+json", "Authorization": f"Bearer {token}"}
        self.base_url = f"https://{location}.azuredatabricks.net/api/2.0/preview/scim/v2"
        self.users_file = users_file
        self._existing_users: Dict[str, str] = {}
        self._new_users: List[str] = []
        self._admin_group_id: str = ""

    @property
    def existing_users(self) -> Dict[str, str]:
        return self._existing_users or self.get_users()

    @property
    def new_users(self) -> List[str]:
        return self._new_users or self.read_user_list()

    @property
    def admin_group_id(self) -> str:
        return self._admin_group_id or self.get_admin_group_id()

    def get_admin_group_id(self) -> str:
        url = f"{self.base_url}/Groups"
        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()

        groups = response.json()["Resources"]
        for group in groups:
            if group["displayName"] == "admins":
                admin_group_id = group["id"]
                self._admin_group_id = admin_group_id
                return admin_group_id

        raise ValueError("Not able to find any groups named 'admins'")

    def add_user(self, user_email: str) -> None:
        body = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "userName": user_email,
            "groups": [{"value": self.admin_group_id}],
        }

        url = f"{self.base_url}/Users"
        response = requests.post(url=url, json=body, headers=self.header)
        response.raise_for_status()

    @staticmethod
    def get_user_id(user_email: str, users: List[Dict]) -> str:
        for user in users:
            if user["userName"] == user_email:
                return user["id"]

        raise ValueError(f"User with user_email {user_email} not found.")

    def delete_user(self, user_id: str) -> None:
        url = f"{self.base_url}/Users/{user_id}"
        response = requests.delete(url=url, headers=self.header)
        response.raise_for_status()

    def get_users(self) -> Dict[str, str]:
        url = f"{self.base_url}/Users"
        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()
        response_json = response.json()
        if "Resources" in response_json:
            user_data = response.json()["Resources"]
            name_to_id = {user["userName"]: user["id"] for user in user_data}
        else:
            name_to_id = {}
        self._existing_users = name_to_id
        return name_to_id

    def read_user_list(self) -> List[str]:
        ws = xlrd.open_workbook(self.users_file).sheet_by_index(0)
        new_users = list(map(lambda x: x.replace("cognite.com", "cognitedata.com").lower(), ws.col_values(0)))
        self._new_users = new_users
        return new_users

    def run_handler(self, handler: Callable[[str], None], should_exist: bool):
        for i, user in enumerate(self.new_users, start=1):
            print(f"Handling {user} ({i}/{len(self.new_users)})")
            if (user in self.existing_users) == should_exist:
                handler(user)
            else:
                print(f"Skipping user {user}, as he/she {'does not exist' if should_exist else 'already exists'}")

    def run(self, action: Action) -> None:
        user_handler = self
        if action == Action.DELETE:
            self.run_handler(lambda u: user_handler.delete_user(user_handler.existing_users[u]), should_exist=True)
        elif action == Action.ADD:
            self.run_handler(lambda u: user_handler.add_user(u), should_exist=False)
