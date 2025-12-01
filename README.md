# Football Data Engineering Pipeline

A data engineering project that extracts, transforms, and loads football (soccer) data from the API-Sports.io API into a SQLite database using an ETL pipeline orchestrated with Apache Airflow.

## Project Structure

```
final_project/
├── api/                      # ETL pipeline modules
│   ├── __init__.py
│   ├── dags.py              # Airflow DAG definitions
│   ├── etl.py               # Main ETL orchestration
│   ├── extract.py           # API data extraction
│   ├── load.py              # Database loading functions
│   └── transform.py         # Data transformation logic
├── app/                     # Application modules
│   └── dashboard.py         # Data visualization dashboard (WIP)
├── db/                      # Database schema definitions
│   ├── __init__.py
│   └── schemas.py           # SQLite table schemas and creation
├── config.toml              # Configuration file
└── requirements.txt         # Python dependencies
```

## ⚠️ Work in Progress

This project is currently under active development. The core ETL pipeline is functional, but several features remain to be implemented.
