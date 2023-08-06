#!/usr/bin/env python

#import plasmacli.component_manager as component_manager
#import plasmacli.workflow_manager as workflow_manager
#import plasmacli.project_manager as project_manager
#
from cometcli.utils import connect_comet, get_comet_status
import cometcli.datasets as datasets
import cometcli.query as query
import click
import os
import collections


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
def cli():
    pass


@click.command(name="status", help="get comet status")
def get_status():
    get_comet_status()


@click.argument('auth_key', required=True)
@click.command(name="connect", help="connect comet to space")
def connect(auth_key):
    connect_comet(auth_key)


@click.command(name="configure", help="configure comet settings")
def configure():
    # pass
    pass

# dataset command group


@click.group(cls=OrderedGroup, help="manage datasets on comet")
def dataset(name='dataset'):
    pass


@click.command(name="list", help="list datasets indexed on comet")
def list_datasets():
    datasets.list_datasets()


@click.command(name="add", help="add datasets to comet")
@click.argument('dataset_path', required=True)
def add_dataset(dataset_path):
    datasets.add_dataset(dataset_path)


@click.command(name="remove", help="remove dataset from comet")
@click.argument('dataset_path', required=True)
def remove_dataset(dataset_path):
    datasets.remove_dataset(dataset_path)


@click.command(name="get", help="download a remote dataset")
@click.argument('dataset_name', required=True)
def get_dataset(dataset_name):
    datasets.get_dataset(dataset_name)


@click.command(name="configure", help="configure dataset")
@click.argument('dataset_name', required=True)
def configure_dataset(dataset_name):
    datasets.configure_dataset(dataset_name)


# query command group

@click.group(cls=OrderedGroup, help="manage queries on comet")
def query(name='query'):
    pass


@click.command(name="list", help="view submitted queries")
def list_queries():
    query.list_queries()


@click.command(name="run", help="execute a query on a dataset")
@click.argument('dataset_name', required=True)
@click.argument('query', required=True)
def execute_query(dataset_name, query):
    query.execute_query(dataset_name, query)


@click.command(name="export", help="export results of a query to a file")
@click.argument('query_id', required=True)
@click.argument('output_file', required=True)
def fetch_query_results(query_id, output_file):
    query.export_query_results(query_id, output_file)


def build_cli():
    dataset.add_command(list_datasets)
    dataset.add_command(add_dataset)
    dataset.add_command(remove_dataset)
    dataset.add_command(get_dataset)
    dataset.add_command(configure_dataset)
    query.add_command(list_queries)
    query.add_command(execute_query)
    query.add_command(fetch_query_results)
    cli.add_command(get_status)
    cli.add_command(connect)
    cli.add_command(configure)
    cli.add_command(dataset)
    cli.add_command(query)
    return cli


def main():
    cli = build_cli()
    cli()


if __name__ == "__main__":
    main()
