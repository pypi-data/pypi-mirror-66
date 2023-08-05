from dv_pyclient.grpc import datasource_manager as ds
from dv_pyclient.grpc import dataSources_pb2_grpc as rpc
import pandas as pd
from io import StringIO
from concurrent import futures
import logging
import grpc
import time
from threading import Timer

def load_test_data():
    # Some import parameters
    ds_id = "ds_id_test_grpc"
    ds_name = "Test Datasource (grpc)"

    sample_data = """
date,trans,symbol,qty,price,currency
2006-01-01,BUY,RHAT,100,35.00,USD
2006-02-01,BUY,RHAT,200,32.00,USD
2006-03-01,BUY,RHAT,300,34.00,USD
2006-04-01,BUY,RHAT,400,35.10,USD
2006-05-01,BUY,RHAT,500,35.20,USD
2006-06-01,BUY,RHAT,600,35.30,USD
2006-01-02,SELL,RHAT,100,35.60,USD
2006-02-02,SELL,RHAT,200,32.60,USD
2006-03-02,SELL,RHAT,300,34.60,USD
2006-04-02,SELL,RHAT,400,35.60,USD
2006-05-02,SELL,RHAT,500,35.60,USD
2006-06-02,SELL,RHAT,600,35.60,USD
2006-01-01,BUY,MSFT,1100,135.00,USD
2006-02-01,BUY,MSFT,1200,132.00,USD
2006-03-01,BUY,MSFT,1300,134.00,USD
2006-04-01,BUY,MSFT,1400,135.10,USD
2006-05-01,BUY,MSFT,1500,135.20,USD
2006-06-01,BUY,MSFT,1600,135.30,USD
2006-01-02,SELL,MSFT,1100,135.60,USD
2006-02-02,SELL,MSFT,1200,132.60,USD
2006-03-02,SELL,MSFT,1300,134.60,USD
2006-04-02,SELL,MSFT,1400,135.60,USD
2006-05-02,SELL,MSFT,1500,135.60,USD
2006-06-02,SELL,MSFT,1600,135.60,USD
"""
    return pd.read_csv(StringIO(sample_data), sep=",", parse_dates=['date'])


def download_covid_us() -> pd.DataFrame:
    index = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_',
             'Combined_Key']

    df_us_confirmed = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")

    df_us_meta = df_us_confirmed[index]
    df_us_confirmed = df_us_confirmed \
        .melt(id_vars=index, var_name="date", value_name="confirmed") \
        .sort_values(by=index + ['date'])


    df_us_deaths_raw = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

    df_us_population = df_us_deaths_raw[index + ['Population']]

    df_us_death = df_us_deaths_raw \
        .melt(id_vars=index, var_name="date", value_name="deaths") \
        .sort_values(by=index + ['date'])

    joined = df_us_death.join(df_us_population, rsuffix='_right', on='UID')
    overlap_cols = list(filter(lambda c: c.endswith('_right'), list(joined.columns)))
    joined.drop(overlap_cols, axis=1, inplace=True)

    joined = joined.join(df_us_confirmed, rsuffix="_right")
    overlap_cols = list(filter(lambda c: c.endswith('_right'), list(joined.columns)))
    joined.drop(overlap_cols, axis=1, inplace=True)

    return joined

def reload_pandas_df(ds_manager, ds_id, ds_name, load_func, seconds_between):
    new_df = ds.PandasDatasource(ds_id, ds_name, load_func())
    ds_manager.addDataSource(ds_id, ds_name, new_df)
    print(f"Updated datasource {ds_name} - {time.time()}")
    Timer(seconds_between, reload_pandas_df, (ds_manager, ds_id, ds_name, load_func, seconds_between)).start()


# Run the server and server your datasource
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_port = 50051

    ds_manager = ds.DataSourceManager()

    # A test pandas datasource
    test_df = load_test_data()
    test_df_id = "my_assigned_ds_id"
    test_df_name = "my_stock_trans"
    test_datasource_pd = ds.PandasDatasource(test_df_id, test_df_name, test_df)
    ds_manager.addDataSource(test_df_id, test_df_name, test_datasource_pd)

    # A John Hopkins Covid ds
    jhu_df = download_covid_us()
    jhu_df_id = "jhu_ds_id"
    jhu_df_name = "John Hopkins Univ, Covid-19 US data"
    jhu_datasource_pd = ds.PandasDatasource(jhu_df_id, jhu_df_name, jhu_df)
    ds_manager.addDataSource(jhu_df_id, jhu_df_name, jhu_datasource_pd)

    # Setup if required periodic reload (test_df)
    reload_pandas_df(ds_manager, test_df_id, test_df_name, load_test_data, 60*60)  #time in seconds
    reload_pandas_df(ds_manager, jhu_df_id, jhu_df_name, download_covid_us, 60*60)

    # Start the RPC server with the configured manager
    rpc.add_RemoteDataSourceServicer_to_server(ds_manager, server)
    server.add_insecure_port(f'[::]:{server_port}')
    server.start()
    print(f"Started server on port {server_port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
