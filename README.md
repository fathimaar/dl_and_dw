# Data Lakes and Data Warehouses: README.md
This repository contains the collaborated work contributed for the module datalakes and data warehouses. This is an academic project for the Masters program, Masters of Science in Applied information and Data Sciences

Authors:
Fathima Abdul Rahman, Email: fathima.abdulrahman@stud.hslu.ch
Justin Dreyer, Email: justin.dreyer@stud.hslu.ch

This repository will provide you with the data required to build a dashboard containing all relevent inflation and demographic data for individual countries, in order to tackle todays pension crisis.

- "Excel_from_S3.py", is a DAG designed to be run in Apache Airflow that fetches relevenet OECD data from an excel workbook stored in an S3 bucket.
- "CPI_Web_Scrape.py", is a DAG that makes use of the IMF API to scrape CPI data, clean the data and input each countries CPI data as a table in Amazon RDS. 
- In order to run Excel_from_S3.py and CPI_Web_Scrape.py simply create a folder named "dags" whithin your airflow file and add these DAGs to the "airflow/dags" folder. 
- "DL_DW.ipynb", is a colab notebook that was developed to extract data from the world bank using the world bank API. The code is used to extract data on development indicators for all the countries.
