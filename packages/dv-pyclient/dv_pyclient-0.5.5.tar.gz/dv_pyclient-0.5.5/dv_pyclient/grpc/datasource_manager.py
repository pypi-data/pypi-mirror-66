from dv_pyclient.grpc import dataSources_pb2 as api
from dv_pyclient.grpc import dataSources_pb2_grpc as rpc
from dv_pyclient.grpc import datasource_util as ds_util
import pandas as pd
import grpc
import copy


class DataSourceManager(rpc.RemoteDataSourceServicer):

    def __init__(self):
        self.ds_manager = {}

    def addDataSource(self, id: str, name: str, df: pd.DataFrame):
        print(f"Adding datasource {name}")
        self.ds_manager[id] = {'name': name, 'df': df}

    def ListDataSources(self, request: api.ListDataSourcesRequest, context) -> api.ListDataSourcesReply:
        datasources = []
        for ds_id in self.ds_manager:
            datasources.append(api.DataSourceResult(id=ds_id, name=self.ds_manager[ds_id]['name']))
        return api.ListDataSourcesReply(dataSources=datasources)

    def dataSourceQuery(self, request: api.DataSourceQueryRequest, context):
        # print("dataSourceQuery", MessageToJson(request))
        if any(map(lambda query: query.dataSourceId not in self.ds_manager.keys(), request.lineQueries)):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Unknown dataSourceId for query. Must be: {self.ds_manager.keys()}')
            raise RuntimeError('Invalid dataSourceQuery request')

        for line_query in request.lineQueries:
            ds = self.ds_manager[line_query.dataSourceId]
            df = ds['df']
            yield from ds_util.dataSourceQueryStreamPandas(df, request)

    def dataSourceUniques(self, request: api.DataSourceUniquesRequest, context):
        # print("dataSourceUniques", MessageToJson(request))
        try:
            datasource = self.ds_manager[request.dataSourceId]
            df = datasource['df']
        except:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid dataSourceUnique request, dataSourceId not found')
            raise RuntimeError('Invalid dataSourceUnique request, dataSourceId not found')

        yield from ds_util.dataSourceUniquesStreamPandas(df, request)

    def sampleDataSourceMeta(self, request: api.DataSourceMetaRequest, context) -> api.DataSourceMetaReply:
        # print("sampleDataSourceMeta", MessageToJson(request))
        try:
            datasource = self.ds_manager[request.dataSourceId]
            ds_name = datasource['name']
            df = datasource['df']
        except:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid sampleDataSourceMeta request, dataSourceId not found')
            raise RuntimeError('Invalid sampleDataSourceMeta request, dataSourceId not found')

        result = ds_util.getDatasourceMetaReplyPandas(df, request.dataSourceId, ds_name)
        context.set_code(grpc.StatusCode.OK)
        return result
