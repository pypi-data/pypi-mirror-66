import os
from typing import Dict, List


def create_dir(path: str) -> None:
    if path and not os.path.exists(path):
        os.mkdir(path)


def write_list(path: str, header: str, lines: List[str]) -> None:
    create_dir(os.path.dirname(path))
    with open(path, "a") as f:
        f.write("---------------------------\n")
        f.write(header + "\n")
        f.writelines(list(map(lambda l: l + "\n", lines)))
        f.write("\n")


def write_dict_with_lists(path: str, d: Dict) -> None:
    create_dir(os.path.dirname(path))
    with open(path, "a") as f:
        for key, lines in d.items():
            f.write(f"{key}\n")
            f.writelines(list(map(lambda l: l + "\n", lines)))
            f.write("\n")
