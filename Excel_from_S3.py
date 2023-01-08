import datetime
import logging
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

#
# TODO: Define a function for the PythonOperator to call and have it log something
#
def excel_from_S3():
    import pandas as pd
    link ='https://justinawsbucket.s3.us-east-1.amazonaws.com/Pension-Markets-in-Focus-2021.xlsx?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECwaCWV1LXdlc3QtMiJHMEUCIHwacyZOfRfohniZcPQX8cwRABuybTUI4aDPJPApbXQpAiEAhnC19xmNOsz4%2FyyZeIlU3LItgO0L%2Bn1%2BNt1RE%2FLLWP8q5wIIZRAAGgw1NDkyODY5Nzk5NTIiDEPu%2B6Zg2idxVrBaZirEAoa08wpWfVeWo9MDCEBGlf%2BVKsb%2FWBFrjFFmDsOpM7Y1spuYcnbqltz4PqgxmgrE3RRpneuZf0YVrKfbh26nBEhCJEaUORFII82lshvf6c0A8%2BZbDv81QfDW3YsJwylWKnPvNHipjcxjAijJhYeuB1yOH819wimaten57RMtgIfEPkhY9HSGXhcwA%2FztHj%2FRCSgGbJEDbl%2Btn82zFeQk2ZzXxG4diNAsrph0%2FgYldnhpRjuL91fVNTPhdP5x2lK%2B%2Fqq0cZONyKepFewuaAm5GQvmw1QNaLkIGiiwQ0u%2FO9fUqpEMqCaZTtgaE3oz3jXk1Mrh%2B%2F2XclYUFvmS2MXELkWY8tIAU%2FLfHZ5PhPYCOwLbwrGWYoIj8vXoH1PBW26WkusoIkwH%2BcZ8JFJ7QkeuzqGFxH4%2FTqnoN9TCUXHSW8ABupv9pDCl1oKdBjqHAsnEttxInSp1duatNCceet4%2FQEjNcgSPR1pIlu9duToG9Xop73TsBjd6ziKgcvXKltVArotuku3gms7teHl1GVHotSMUSfCNIaBkDIzeV9iGSs5unrJowtcKXv%2Ft7%2FhejEXuCd6T8U6DDaR93pcn9RVuS7P%2BGe1WBD4%2B69Z19NL6XaxBBN6%2Bi%2BEN%2F4B5sKaCD3qqfqq8mOFMb88tewtOjtxTfMoM%2Bxtve%2BqlsPr3XBO00E1dkS%2B2ukOUamF6aE1rt%2BsGMp64%2B942vkLCcR689IR4pAViK6vp9cV6eLzh%2Bm5UYe4wBHcijxrTtbyNzgyvuAK9r%2F8aoLJX5SMsZYn6EyYZKixzz2sI&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221219T200022Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAX7ZAOFFYA4KQWCUV%2F20221219%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=79597f8f68f6c7b087acb78503f8c07655546e186085054c43b52060e085a420'
    data = pd.read_excel(link,'Figure 1.3')
    data1= data
    df = data1.iloc[2:,0:3]
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={ df.columns[0]: "Country" }, inplace = True)
    #Table 2
    df_read = pd.read_excel(link,'Figure 1.15')
    df2=df_read
    df2 = df2.iloc[1:,0:6]
    new_header2 = df2.iloc[0] #grab the first row for the header
    df2 = df2[1:] #take the data less the header row
    df2.columns = new_header2 #set the header row as the df header
    df2.rename(columns={ df2.columns[0]: "Country" }, inplace = True)
    del df2["CIS (when look-through unavailable)"]
    import psycopg2
    import sqlalchemy
    from sqlalchemy import create_engine
    
    engine = create_engine("postgresql+psycopg2://Justin:12345678@datalake.c987a5jhnrsw.us-east-1.rds.amazonaws.com:5432/datalake")

    df.to_sql('Total_assets',engine, if_exists='replace')
    df2.to_sql('Allocation_assets', engine, if_exists='replace')

args = {
    'owner': 'Justin Dreyer',
    'start_date': datetime.datetime.now()

}

#defining the dag object
dag = DAG(
    dag_id='excel_from_S3',
    default_args=args,
    schedule_interval='@monthly' #weekly
)

#assigning the task for our dag to do
with dag:
    scrape_cpi_data = PythonOperator(
        task_id='excel_fromS3',
        python_callable=excel_from_S3,
        provide_context=True
    )


