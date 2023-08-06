import os
import sys

import click

from cognite.databricks_utils.jobs import JobChecker
from cognite.databricks_utils.scopes import ScopeChecker
from cognite.databricks_utils.users import Action, UsersHandler

loc_option = click.option("--loc", default="westeurope", type=click.Choice(["westeurope", "northeurope"]))
token_option = click.option("--token", default=os.environ.get("TOKEN"), help="Databricks token")


@click.group()
def db():
    """Databricks administrator utilities.
    """
    pass


@db.command()
@token_option
@loc_option
@click.option(
    "--action",
    default=Action.ADD.value,
    type=click.Choice(map(lambda a: a.value, Action.__members__.values())),
    help="Add or delete users",
)
@click.option("--input-file", default="users.xlsx", help="Relative path to excel file with user emails")
def users(action, token, location, input_file):
    """
    Add or delete users in a Databricks shard
    """
    check_token(token)
    handler = UsersHandler(location=location, token=token, users_file=input_file)
    handler.run(Action(action))


@db.command()
@token_option
@loc_option
def scopes(token, location):
    """
    Get metadata about all scopes in a Databricks shard
    """
    check_token(token)
    checker = ScopeChecker(location=location, token=token)
    checker.run()
    checker.write_results_to_file("results/scopes_results.txt")


@db.command()
@token_option
@loc_option
def jobs(token, location):
    """
    Get metadata about all jobs in a Databricks shard
    """
    check_token(token)
    checker = JobChecker(location=location, token=token)
    checker.run()
    checker.write_results_to_file("results/jobs_results.txt")


def check_token(token):
    if not token:
        print("Expected a Databricks token to be set as a environment variable named 'TOKEN'")
        sys.exit(1)


def run():
    db()
