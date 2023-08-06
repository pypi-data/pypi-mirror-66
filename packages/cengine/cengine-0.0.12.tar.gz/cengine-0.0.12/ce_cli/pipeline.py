import os
from datetime import datetime, timezone
from pathlib import Path

import click
import yaml
from click import pass_context
from tabulate import tabulate

import ce_api
from ce_api.enums import PipelineStatusTypes
from ce_api.models import PipelineCreate, PipelineUpdate
from ce_cli import constants
from ce_cli.cli import cli
from ce_cli.utils import api_client, api_call, download_artifact
from ce_cli.utils import check_login_status, pass_info, save_config
from ce_cli.utils import get_workers_cpus_from_env_config
from ce_cli.utils import notice, error, declare, confirmation


@cli.group()
@pass_info
def pipeline(info):
    """Create, configure and deploy pipeline runs"""
    check_login_status(info)

    user = info[constants.ACTIVE_USER]

    # WORKSPACE AND DATASOURCE
    if constants.ACTIVE_WORKSPACE in info[user]:
        api = ce_api.WorkspacesApi(api_client(info))
        ws = api_call(api.get_workspace_api_v1_workspaces_workspace_id_get,
                      info[user][constants.ACTIVE_WORKSPACE])

        click.echo('You are working on the workspace:')
        declare('ID: {}\nName: {}\n'.format(ws.id, ws.name))
    else:
        raise click.ClickException(message=error(
            "You have not set a workspace to work on yet \n"
            "'cengine workspace list' to see the possible options \n"
            "'cengine workspace set' to select a workspace \n"))


@pipeline.group('configure', invoke_without_command=True, chain=True)
@click.option('--input_path', default=None,
              help='Path to an initial config file')
@click.option('--output_path', required=True, help='Path to save the config')
@pass_info
@pass_context
def configure_pipeline(context, info, output_path, input_path):
    """Configure pipeline from scratch"""
    # INTRODUCTION
    notice('\nIn the Core Engine, the creation of a pipeline is achieved '
           'through a configuration file. This function will help you create '
           'such a configuration file and store it locally. '
           'While you push a pipeline, you will be required to provide this '
           'file. \n\nPlease note that, before you push your pipeline, you '
           'can still manually modify it even further according to your '
           'needs.\n')

    user = info[constants.ACTIVE_USER]

    if constants.ACTIVE_DATASOURCE in info[user]:

        api = ce_api.DatasourcesApi(api_client(info))
        ds = api_call(
            api.get_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_get,
            info[user][constants.ACTIVE_DATASOURCE])

        click.echo('You are working on the datasource:')
        declare('ID: {}\nName: {}\n'.format(ds.id, ds.name))
    else:
        raise click.ClickException(message=error(
            "You have not set a datasource to work on yet \n"
            "'cengine datasource list' to see the possible options \n"
            "'cengine datasource set' to select a datasource \n"))


@pipeline.command('pull')
@click.argument('pipeline_id', type=click.INT)
@click.option('--output_path',
              default=os.path.join(os.getcwd(), 'ce_config.yaml'))
@pass_info
def pull_pipeline(info, pipeline_id, output_path):
    """Copy the configuration of a registered pipeline"""
    active_user = info[constants.ACTIVE_USER]
    workspace_id = info[active_user][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))
    pp = api_call(
        api.get_workspaces_pipeline_by_id_api_v1_workspaces_workspace_id_pipelines_pipeline_id_get,
        workspace_id=workspace_id,
        pipeline_id=pipeline_id)

    c = pp.exp_config
    if 'bq_args' in c:
        c.pop('bq_args')
    if 'ai_platform_training_args' in c:
        c.pop('ai_platform_training_args')

    save_config(c, output_path)


@pipeline.command('push')
@click.argument('config_path')
@click.argument('pipeline_name')
@click.option('--workers', required=False, type=int)
@click.option('--cpus_per_worker', required=False, type=int)
@pass_info
def push_pipeline(info,
                  config_path,
                  pipeline_name,
                  workers,
                  cpus_per_worker):
    """Register a pipeline with the selected configuration"""
    active_user = info[constants.ACTIVE_USER]
    if constants.ACTIVE_DATASOURCE in info[active_user]:
        api = ce_api.DatasourcesApi(api_client(info))
        ds = api_call(
            api.get_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_get,
            info[active_user][constants.ACTIVE_DATASOURCE])

        click.echo('You are working on the datasource:')
        declare('ID: {}\nName: {}\n'.format(ds.id, ds.name))
    else:
        raise click.ClickException(message=error(
            "You have not set a datasource to work on yet \n"
            "'cengine datasource list' to see the possible options \n"
            "'cengine datasource set' to select a datasource \n"))

    with open(config_path, 'rt', encoding='utf8') as f:
        config = yaml.load(f)

    workspace_id = info[active_user][constants.ACTIVE_WORKSPACE]
    datasource_id = info[active_user][constants.ACTIVE_DATASOURCE]

    if cpus_per_worker is None and workers is None:
        notice("No pipeline configuration provided. Automagically configuring "
               "the best settings based on your datasource.\n")
    elif cpus_per_worker is None and workers is None:
        pass
    else:
        error("Please set either both of `cpus_per_worker` and `workers` or "
              "none of them.")

    api = ce_api.PipelinesApi(api_client(info))
    p = api_call(api.create_pipeline_api_v1_pipelines_post,
                 PipelineCreate(name=pipeline_name,
                                workers=workers,
                                cpus_per_worker=cpus_per_worker,
                                exp_config=config,
                                datasource_id=datasource_id,
                                workspace_id=workspace_id))
    declare('Pipeline {id} pushed successfully!'.format(id=p.id))

    workers, cpus_per_worker = get_workers_cpus_from_env_config(p.env_config)

    declare('The pipeline has been configured to run with {} workers at {} '
            'cpus per worker. \nTo change, please run '
            '`cengine pipeline update {} --workers [NEW_NUM_WORKERS] '
            '--cpus_per_worker [NEW_NUM_CPUS]`\n'.format(
        workers,
        cpus_per_worker,
        p.id,
    ))
    declare("Use `cengine pipeline run {}` to run the pipeline!".format(p.id))


@pipeline.command('run')
@click.argument('pipeline_id')
@click.option('-f', '--force', is_flag=True, default=False,
              help='Force run pipeline with no prompts')
@pass_info
def run_pipeline(info, pipeline_id, force):
    """Initiate the run of a selected pipeline"""
    active_user = info[constants.ACTIVE_USER]
    ws_id = info[active_user][constants.ACTIVE_WORKSPACE]

    # get pipeline
    api = ce_api.PipelinesApi(api_client(info))
    pp = api_call(api.get_pipeline_api_v1_pipelines_pipeline_id_get,
                  pipeline_id)

    # get datasource
    ds_api = ce_api.DatasourcesApi(api_client(info))
    ds = api_call(
        ds_api.get_bigquery_datasource_api_v1_datasources_bigquery_bq_ds_id_get,
        pp.datasource_id)

    # get config
    workers, cpus_per_worker = get_workers_cpus_from_env_config(
        pp.env_config)

    notice('Using datasource ID: {}\nName: {}\n'.format(ds.id, ds.name))
    notice('Setting up your pipeline with {} workers at {} cpus per worker.\n'
           .format(workers, cpus_per_worker))

    if pp.workspace_id != ws_id:
        error('The pipeline does not exist in this workspace! Please try'
              ' workspace {} instead'.format(pp.workspace_id))

    if not force:
        if workers * cpus_per_worker > 100:
            confirmation('This configuration might incur significant charges, '
                         'and you will not be able to cancel the pipeline once'
                         ' its triggered. Are you sure you want to continue?',
                         abort=True)
        else:
            confirmation('You will not be able to cancel the pipeline once '
                         'its triggered. Are you sure you want to continue?',
                         abort=True)

    notice('Provisioning the require resources. '
           'This might take a few minutes..')
    api_call(api.run_pipeline_api_v1_pipelines_pipeline_id_run_post,
             pipeline_id)
    declare('Pipeline {id} is now running!\n'.format(id=pipeline_id))
    declare("Use 'cengine pipeline status --pipeline_id {}' to check on its "
            "status".format(pipeline_id))


@pipeline.command('list')
@pass_info
def list_pipelines(info):
    """List of registered pipelines"""
    notice('Fetching pipeline(s). This might take a few seconds..')
    active_user = info[constants.ACTIVE_USER]
    ws = info[active_user][constants.ACTIVE_WORKSPACE]
    api = ce_api.WorkspacesApi(api_client(info))
    pipelines = api_call(
        api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
        ws)
    pipelines.sort(key=lambda x: x.id)
    statuses = {}
    for count, p in enumerate(pipelines):
        statuses[p.id] = {
            'name': p.name,
        }

    declare('Currently, you have {count} different pipeline(s) in '
            'workspace {ws}.\n'.format(count=len(statuses), ws=ws))

    if len(statuses) > 0:
        table = []
        for k, v in statuses.items():
            table.append({
                'ID': k,
                'Name': v['name'],
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


# TODO: [LOW] Add saved time
@pipeline.command('status')
@click.option('--pipeline_id', required=False, type=click.INT,
              help='Pipeline ID to check status of')
@pass_info
def get_pipeline_status(info, pipeline_id):
    """Get status of started pipelines"""
    notice('Fetching pipelines. This might take a few seconds..')
    active_user = info[constants.ACTIVE_USER]
    ws = info[active_user][constants.ACTIVE_WORKSPACE]
    p_api = ce_api.PipelinesApi(api_client(info))
    api = ce_api.WorkspacesApi(api_client(info))
    billing_api = ce_api.BillingApi(api_client(info))
    if pipeline_id:
        p = api_call(
            api.get_workspaces_pipeline_by_id_api_v1_workspaces_workspace_id_pipelines_pipeline_id_get,
            workspace_id=ws,
            pipeline_id=pipeline_id)
        if p.pipeline_run is None or p.pipeline_run.status == \
                PipelineStatusTypes.NotStarted.name:
            error("Please run this pipeline first!")
        pipelines = [p]
    else:
        pipelines = api_call(
            api.get_workspaces_pipelines_api_v1_workspaces_workspace_id_pipelines_get,
            workspace_id=ws)
        pipelines.sort(key=lambda x: x.id)

    statuses = {}
    with click.progressbar(
            label='Fetching pipeline statuses',
            length=len(pipelines)) as bar:
        for count, p in enumerate(pipelines):
            # if its not started, then don't call the metrics API
            if p.pipeline_run is None or p.pipeline_run.status == \
                    PipelineStatusTypes.NotStarted.name:
                continue

            run = api_call(
                p_api.get_pipeline_run_api_v1_pipelines_pipeline_id_run_get,
                pipeline_id=p.id)

            if run.status != PipelineStatusTypes.Running.name:
                billing = api_call(
                    billing_api.get_pipeline_billing_api_v1_billing_pipeline_id_get,
                    p.id,
                )
                compute_cost = billing.compute_cost
                train_cost = billing.training_cost
                saved_cost = billing.saved_cost
            else:
                compute_cost = 0
                train_cost = 0
                saved_cost = 0
            bar.update(count)

            statuses[p.id] = {
                'pipeline_status': run.status,
                'name': p.name,
                'compute_cost': compute_cost,
                'training_cost': train_cost,
                'total_cost': compute_cost + train_cost,
                'saved_cost': saved_cost,
            }
            if len(run.components_status):
                total_components = len(run.components_status)
            else:
                total_components = 1  # avoid zero division error
            n_successful_components = \
                len([c for c in run.components_status if
                     c['status'] == PipelineStatusTypes.Succeeded.name])
            statuses[p.id]['completion'] = round(
                n_successful_components / total_components * 100)
            if run.kubeflow_end_time:
                statuses[p.id]['time'] = run.kubeflow_end_time - \
                                         run.run_time
            else:
                statuses[p.id]['time'] = datetime.now(timezone.utc) - \
                                         run.run_time
            statuses[p.id]['start_time'] = run.run_time
            statuses[p.id]['end_time'] = run.kubeflow_end_time
        bar.update(len(pipelines))

    declare('Currently, you have run {count} different '
            'pipeline(s).\n'.format(count=len(statuses)))

    if len(statuses) > 0:
        table = []
        for k, v in statuses.items():
            table.append({
                'ID': k,
                'Name': v['name'],
                'Pipeline Status': v['pipeline_status'],
                'Completion': str(v['completion']) + '%',
                'Compute Cost (€)': round(v['compute_cost'], 4),
                'Training Cost (€)': round(v['training_cost'], 4),
                'Total Cost (€)': round(v['total_cost'], 4),
                'Execution Time': v['time'],
            })
        click.echo(tabulate(table, headers='keys', tablefmt='presto'))
        click.echo()


@pipeline.command('statistics')
@click.argument('pipeline_id', type=int)
@pass_info
def statistics_pipeline(info, pipeline_id):
    """Serve the statistics of a pipeline run"""
    notice('Generating statistics for the pipeline '
           'ID {}. If your browser opens up to a blank window, please refresh '
           'the page once.'.format(pipeline_id))

    ws_id = info[info[constants.ACTIVE_USER]][constants.ACTIVE_WORKSPACE]

    import panel as pn
    import tensorflow_data_validation as tfdv
    from tensorflow_data_validation.utils.display_util import \
        get_statistics_html
    from tensorflow_metadata.proto.v0.statistics_pb2 import \
        DatasetFeatureStatisticsList

    api = ce_api.PipelinesApi(api_client(info))
    artifact = api_call(
        api.get_pipeline_artifacts_api_v1_pipelines_pipeline_id_artifacts_component_type_get,
        pipeline_id=pipeline_id,
        component_type='StatisticsNonSequence')

    path = Path(click.get_app_dir(constants.APP_NAME), 'statistics',
                str(ws_id), str(pipeline_id))

    result = {}
    for split in ['train', 'eval']:
        d_path = os.path.join(path, split)

        for a in artifact:
            if a['children'] and split in a['children'][0]['signed_url']:
                download_artifact(artifact_json=a, path=d_path)

        stats_path = os.path.join(d_path, 'stats_tfrecord')
        stats = tfdv.load_statistics(stats_path)

        dataset_list = DatasetFeatureStatisticsList()
        for i, d in enumerate(stats.datasets):
            if d.name == 'All Examples':
                d.name = split
                dataset_list.datasets.append(d)
        result[split] = dataset_list

    h = get_statistics_html(result['train'], result['eval'], 'train', 'eval')

    pn.serve(panels=pn.pane.HTML(h, width=1200), show=True)


@pipeline.command('model')
@click.argument('pipeline_id', type=int)
@click.option('--output_path', required=True, help='Path to save the model')
@pass_info
def model_pipeline(info, pipeline_id, output_path):
    """Download the trained model to a specified location"""
    if os.path.exists(output_path) and os.path.isdir(output_path):
        if not [f for f in os.listdir(output_path) if
                not f.startswith('.')] == []:
            error("Output path must be an empty directory!")
    if os.path.exists(output_path) and not os.path.isdir(output_path):
        error("Output path must be an empty directory!")
    if not os.path.exists(output_path):
        "Creating directory {}..".format(output_path)

    notice('Downloading the trained model from pipeline '
           'ID {}. This might take some time if the model '
           'resources are significantly large in size.\nYour patience is '
           'much appreciated!'.format(pipeline_id))

    api = ce_api.PipelinesApi(api_client(info))
    artifact = api_call(
        api.get_pipeline_artifacts_api_v1_pipelines_pipeline_id_artifacts_component_type_get,
        pipeline_id=pipeline_id,
        component_type='Trainer')

    # TODO: maybe add a progress bar here for the download
    if len(artifact) == 1:
        download_artifact(artifact_json=artifact[0],
                          path=output_path)
    else:
        error('Something unexpected happened! Please contact '
              'core@maiot.io to get further information.')

    declare('Model downloaded to: {}'.format(output_path))


@pipeline.command('update')
@click.argument('pipeline_id', type=int)
@click.option('--workers', required=True, type=int)
@click.option('--cpus_per_worker', required=True, type=int)
@pass_info
def update_pipeline(info,
                    pipeline_id: int,
                    workers: int,
                    cpus_per_worker: int):
    """Update a pipelines configuration"""
    api = ce_api.PipelinesApi(api_client(info))
    p = api_call(api.update_pipeline_api_v1_pipelines_pipeline_id_put,
                 PipelineUpdate(workers=workers,
                                cpus_per_worker=cpus_per_worker),
                 pipeline_id=pipeline_id)
    declare('Pipeline {id} updated successfully!'.format(id=p.id))
    workers, cpus_per_worker = get_workers_cpus_from_env_config(p.env_config)
    declare('The pipeline has been configured to run with {} workers at {} '
            'cpus per worker. \nTo change, please run '
            '`cengine pipeline update {} --workers [NEW_NUM_WORKERS] '
            '--cpus_per_worker [NEW_NUM_CPUS]`'.format(
        workers,
        cpus_per_worker,
        p.id,
    ))
    declare("Use `cengine pipeline run {}` to run the pipeline!".format(p.id))
