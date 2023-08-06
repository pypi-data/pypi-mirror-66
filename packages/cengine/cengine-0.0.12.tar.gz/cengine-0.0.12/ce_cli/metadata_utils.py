from typing import Text, List, Dict, Any

import pandas as pd


class CoreEngineMDStore:

    def __init__(self,
                 uri: Text = None):
        """
        Constructor or the MD Store for the maiot Core Engine
        :param uri: the path to the metadata store
        """
        self.store = self.initiate_store(uri)

    @staticmethod
    def initiate_store(uri):
        """
        Initiates the configuration of the store
        :param uri: path the the metadata store
        :return: the instance of the MD Store
        """
        # only import these when needed, otherwise they slow CLI down
        from ml_metadata.metadata_store import metadata_store
        from ml_metadata.proto import metadata_store_pb2

        config = metadata_store_pb2.ConnectionConfig()
        config.sqlite.filename_uri = uri
        return metadata_store.MetadataStore(config)

    def visualize_contexts(self):
        """
        Creates a DataFrame of the available contexts
        :return: pd.DataFrame
        """
        context_df = pd.DataFrame(columns=['run_id',
                                           'pipeline_name',
                                           'context_name'])
        for c in self.store.get_contexts():
            context_df.loc[c.id] = pd.Series({
                'context_name': c.name,
                'run_id': c.properties['run_id'].string_value,
                'pipeline_name': c.properties['pipeline_name'].string_value})
        return context_df

    def list_registered_components(self):
        """
        returns a list of registered components
        :return: list
        """
        executions = self.store.get_executions()
        component_list = list({e.properties['component_id'].string_value
                               for e in executions})
        return component_list

    def filter_executions_by_component(self, component):
        assert component in self.list_registered_components()
        executions = self.store.get_executions()
        return [e for e in executions
                if e.properties['component_id'].string_value == component]

    def filter_executions_by_condition(self, condition):
        component = condition['component']
        property_name = condition['property_name']
        value = condition['value']

        executions = self.filter_executions_by_component(component)
        return [e for e in executions
                if e.properties[property_name].string_value == value]

    def map_execution_to_context(self, executions):
        return [self.store.get_contexts_by_execution(e.id)[0]
                for e in executions]

    def list_contexts_by_condition(self, condition):
        executions = self.filter_executions_by_condition(condition)
        contexts = self.map_execution_to_context(executions)
        return contexts

    # Got shit done

    def get_outcomes_in_context(self,
                                context_id=None,
                                output_components: List = None):
        """
        :param context_id:
        :param output_components:
        :return:
        """
        if output_components:
            output_ids = output_components
        else:
            output_ids = self.list_registered_components()

        # Among all the executions in context, select the right component
        execs_in_context = self.store.get_executions_by_context(context_id)
        execs_components = {e.properties['component_id'].string_value: e.id
                            for e in execs_in_context
                            if e.properties['component_id'].string_value
                            in output_ids}

        result = {}
        # Get the corresponding event and extract the output artifact ids of it
        for component, exec_id in execs_components.items():
            events = self.store.get_events_by_execution_ids([exec_id])
            artifact_ids = [e.artifact_id for e in events if e.type == 4]
            result[component] = self.store.get_artifacts_by_id(artifact_ids)
        return result

    def get_outcomes(self,
                     context_ids: List[Any] = None,
                     context_names: List[Text] = None,
                     output_components: List[Text] = None,
                     conditions: List[Dict] = None):

        """

        :param context_ids:
        :param context_names:
        :param conditions:
        :param output_components:
        :return:
        """
        if bool(context_ids) and bool(context_names):
            raise Exception("Cant define context id/names at the same time")

        if context_ids:
            target_context_ids = context_ids
        elif context_names:
            target_contexts = self.store.get_contexts()
            target_context_ids = [c.id for c in target_contexts if
                                  c.name in context_names]
        else:
            target_contexts = self.store.get_contexts()
            target_context_ids = [c.id for c in target_contexts]

        if conditions:
            for cond in conditions:
                context_w_cond = self.list_contexts_by_condition(cond)
                context_w_cond_ids = [c.id for c in context_w_cond]
                target_context_ids = [c for c in target_context_ids
                                      if c in context_w_cond_ids]

        result = {}
        for c_id in target_context_ids:
            result[c_id] = self.get_outcomes_in_context(c_id,
                                                        output_components)

        return {k: self.extract_uris(v) for k, v in result.items()}

    @staticmethod
    def extract_uris(result):
        return {k: [a.uri for a in v] for k, v in result.items()}
