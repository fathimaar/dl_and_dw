import datetime
import logging
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

#
# TODO: Define a function for the PythonOperator to call and have it log something
#
def scrape():
    import requests

    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    key = 'CompactData/IFS/M.GB.PCPI_IX' # adjust codes here

    # Navigate to series in API-returned JSON data
    data = (requests.get(f'{url}{key}').json()
            ['CompactData']['DataSet']['Series'])
    ##################################################################
    import pandas as pd          # pandas version 0.23

    baseyr = data['@BASE_YEAR']  # Save the base year

    # Create pandas dataframe from the observations
    data_list = [[obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]
                 for obs in data['Obs']]

    df = pd.DataFrame(data_list, columns=['date', 'value'])

    (df['date']) = pd.to_datetime(df['date'])
    ##################################################################
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    key = 'Dataflow'  # Method with series information
    search_term = 'Price'  # Term to find in series names
    series_list = requests.get(f'{url}{key}').json()\
                ['Structure']['Dataflows']['Dataflow']
    # Use dict keys to navigate through results:
    for series in series_list:
        if search_term in series['Name']['#text']:
            print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")
    ##################################################################
    key = 'DataStructure/CPI'  # Method / series
    dimension_list = requests.get(f'{url}{key}').json()\
                ['Structure']['KeyFamilies']['KeyFamily']\
                ['Components']['Dimension']
    for n, dimension in enumerate(dimension_list):
        print(f"Dimension {n+1}: {dimension['@codelist']}")
    #######################################
    key = f"CodeList/{dimension_list[1]['@codelist']}"
    code_list = requests.get(f'{url}{key}').json()\
            ['Structure']['CodeLists']['CodeList']['Code']
    ###############################
    countries = []
    for i in code_list:
        countries.append(i['@value'])

    #####################
    collection = []
    errors=[]
    for country in countries:

        url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
        key = 'CompactData/IFS/M.{}.PCPI_IX'.format(country) # adjust codes here

    # Navigate to series in API-returned JSON data
        try:
            data = (requests.get(f'{url}{key}').json()
                ['CompactData']['DataSet']['Series'])





    # Create pandas dataframe from the observations

            baseyr = data['@BASE_YEAR']  # Save the base year
            data_list = [[obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]
                for obs in data['Obs']]

            df = pd.DataFrame(data_list, columns=['date', str(country)])

            df['date'] = pd.to_datetime(df['date'])

            collection.append(df)

        except Exception as e:
            errors.append(e)
            continue

    import psycopg2
    import sqlalchemy
    from sqlalchemy import create_engine

    engine = create_engine("postgresql+psycopg2://Justin:12345678@datalake.c987a5jhnrsw.us-east-1.rds.amazonaws.com:5432/datalake")

    for i in range(len(collection)):
        collection[i].to_sql(countries[i],engine, if_exists='replace')



args = {
    'owner': 'Justin Dreyer',
    'start_date': datetime.datetime.now()

}

#defining the dag object
dag = DAG(
    dag_id='cpi_scrape',
    default_args=args,
    schedule_interval='@weekly' #weekly
)

#assigning the task for our dag to do
with dag:
    scrape_cpi_data = PythonOperator(
        task_id='cpi',
        python_callable=scrape,
        provide_context=True
    )




