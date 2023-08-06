import json

import click
from tabulate import tabulate

import ce_api
from ce_api.models import DatasourceBQCreate
from ce_cli import constants
from ce_cli.cli import cli, pass_info
from ce_cli.utils import check_login_status, api_client, api_call, declare


@cli.group()
@pass_info
def datasource(info):
    """Interaction with the available datasources"""
    check_login_status(info)


@datasource.command('list')
@pass_info
def list_datasources(info):
    """List of all datasources available to the user"""
    user = info[constants.ACTIVE_USER]

    api = ce_api.DatasourcesApi(api_client(info))
    # TODO: this shouldnt be limited to BQ
    ds_list = api_call(
        api.get_bigquery_datasources_api_v1_datasources_bigquery_get)

    if constants.ACTIVE_DATASOURCE in info[user]:
        active_datasource = info[user][constants.ACTIVE_DATASOURCE]
    else:
        active_datasource = None

    declare('You have created {count} different '
            'datasource(s).\n'.format(count=len(ds_list)))

    if ds_list:
        table = []
        for ds in ds_list:
            table.append({
                'Selection': '*' if ds.id == active_datasource else '',
                'ID': ds.id,
                'Name': ds.name,
                'Rows': ds.n_rows,
                'Cols': ds.n_columns,
                'Size (MB)': round(ds.n_bytes / (1024 * 1024)),
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


@datasource.command('set')
@click.argument("datasource_id", default=None, type=int)
@pass_info
def set_datasource(info, datasource_id):
    """Set datasource to be active"""
    user = info[constants.ACTIVE_USER]

    api = ce_api.DatasourcesApi(api_client(info))
    ds = api_call(
        api.get_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_get,
        datasource_id)

    info[user][constants.ACTIVE_DATASOURCE] = ds.id
    info.save()
    declare('Active datasource set to id: {id}'.format(id=datasource_id))


# @datasource.command('delete')
# @click.argument("datasource_id", type=int)
# @pass_info
# def delete_datasource(info, datasource_id):
#     api = ce_api.DatasourcesApi(api_client(info))
#     api_call(
#         api.delete_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_delete,
#         datasource_id)
#
#     users = [u for u in info.keys() if u != constants.ACTIVE_USER]
#     for user in users:
#         if constants.ACTIVE_DATASOURCE in info[user] and \
#                 info[user][constants.ACTIVE_DATASOURCE] == datasource_id:
#             info[user].pop(constants.ACTIVE_DATASOURCE)
#
#     info.save()


@datasource.group('create')
@pass_info
def create_datasource(info):
    """Create a datasource. Only BigQuery is allowed for now."""
    pass


@create_datasource.command('bq')
@click.option("--name", default=None, help='Name of the datasource')
@click.option("--project", required=True, help='Project of the BQ table')
@click.option("--dataset", required=True, help='Dataset of the BQ table')
@click.option("--table", required=True, help='Name of the BQ table')
@click.option("--table_type", required=True,
              help='Type of the BQ table, public or private')
@click.option("--service_account", required=False,
              help='Path to the service account')
@pass_info
@click.pass_context
def create_bq_datasource(ctx, info, name, project, dataset, table, table_type,
                         service_account):
    """Create BigQuery datasource and set it to be active"""
    click.echo(
        'Registering the BQ table {}:{}:{}...'.format(project, dataset, table))

    account = None
    if service_account is not None:
        with open(service_account, 'rt', encoding='utf8') as f:
            account = json.load(f)

    api = ce_api.DatasourcesApi(api_client(info))
    ds = api_call(
        api.create_datasource_bigquery_api_v1_datasources_bigquery_post,
        DatasourceBQCreate(name=name,
                           client_project=project,
                           client_dataset=dataset,
                           client_table=table,
                           bigquery_type=table_type,
                           service_account=account))
    declare('Datasource registered.')
    ctx.invoke(set_datasource, datasource_id=ds.id)
