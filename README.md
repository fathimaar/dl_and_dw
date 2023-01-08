# Data Lakes and Data Warehouses: README.md
This repository contains the collaborated work contributed for the module datalakes and data warehouses. This is an academic project for the Masters program, Masters of Science in Applied information and Data Sciences

- "Excel_from_S3.py", is a DAG designed to be run in Apache Airflow that fetches relevenet OECD data from an excel workbook stored in an S3 bucket.
- "CPI_Web_Scrape.py", is a DAG that makes use of the IMF API to scrape CPI data, clean the data and input each countries CPI data as a table in Amazon RDS. 

- In order to run Excel_from_S3.py and CPI_Web_Scrape.py simply create a folder named "dags" whithin your airflow file and add these DAGs to the "airflow/dags" folder. 
