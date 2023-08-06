from typing import Dict, List, Tuple

from databricks_api import DatabricksAPI
from requests import HTTPError

from cognite.databricks_utils.file_util import write_dict_with_lists, write_list


class ScopeChecker:
    def __init__(self, location: str, token: str):
        host = f"https://{location}.azuredatabricks.net"
        self.client = DatabricksAPI(host=host, token=token)
        self.principals: Dict[str, List[str]] = {}
        self.scopes_without_acls: List[str] = []
        self.scopes_with_zero_secrets: List[str] = []

    def get_group_members(self, group_name: str) -> List[Dict[str, str]]:
        try:
            group_info = self.client.groups.get_group_members(group_name)
            if not group_info:
                print(f"Group without group info: {group_name}")
                return []
            return group_info["members"]
        except HTTPError:
            return []

    def add_principal(self, principal_name, scope_name, permission, group_name="", has_secrets: bool = True) -> None:
        if principal_name not in self.principals:
            self.principals[principal_name] = []

        s = (
            f"{scope_name}{f' (through group {group_name})' if group_name else ''} with permissions {permission}."
            f"{' Scope has zero secrets.' if not has_secrets else ''}"
        )

        self.principals[principal_name].append(s)

    def check_if_secrets(self, scope_name: str, secrets: Dict) -> bool:
        if "secrets" in secrets:
            return True
        self.scopes_with_zero_secrets.append(scope_name)
        return False

    def check_scope_have_acl(self, scope_name: str) -> Tuple[bool, List[Dict]]:
        acls = self.client.secret.list_acls(scope=scope_name)
        if "items" not in acls:
            self.scopes_without_acls.append(scope_name)
            return False, []
        return True, acls["items"]

    @staticmethod
    def check_acl_has_principal(acl: Dict[str, str]) -> Tuple[bool, str]:
        if "principal" in acl and "permission" in acl and acl["permission"] == "MANAGE":
            return True, acl["principal"]
        return False, ""

    def add_group_principal(
        self, group_name: str, scope_name: str, members: List[Dict[str, str]], has_secrets: bool
    ) -> None:
        for member in members:
            self.add_principal(
                member["user_name"], scope_name, "MANAGE", group_name=group_name, has_secrets=has_secrets,
            )

    def check_acl(self, scope_name: str, acl: Dict[str, str], has_secrets: bool):
        has_principal, principal = self.check_acl_has_principal(acl)
        if has_principal:
            group_members = self.get_group_members(principal)
            if group_members:
                self.add_group_principal(principal, scope_name, group_members, has_secrets)
            else:
                self.add_principal(principal, scope_name, "MANAGE", has_secrets=has_secrets)

    def check_acls(self, scope_name: str, has_secrets: bool) -> None:
        has_acls, acls = self.check_scope_have_acl(scope_name)
        if has_acls:
            for acl in acls:
                self.check_acl(scope_name, acl, has_secrets)

    def run(self):
        counter = 0
        scopes = self.client.secret.list_scopes()["scopes"]
        for scope in scopes:
            counter += 1
            scope_name = scope["name"]
            print(f"Checking scope named {scope_name} ({counter}/{len(scopes)})")

            if scope["backend_type"] == "AZURE_KEYVAULT":
                continue

            secrets = self.client.secret.list_secrets(scope=scope_name)
            has_secrets = self.check_if_secrets(scope_name, secrets)
            self.check_acls(scope_name, has_secrets)

    def write_results_to_file(self, file_path: str) -> None:
        write_dict_with_lists(file_path, self.principals)
        write_list(file_path, "Scopes without ACLs", self.scopes_without_acls)
        write_list(file_path, "Scopes without secrets", self.scopes_with_zero_secrets)
