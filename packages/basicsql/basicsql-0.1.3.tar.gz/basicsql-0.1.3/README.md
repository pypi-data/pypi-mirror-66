# Basic SQL

This is a small package intended to help with executing (mainly) raw SQL queries for different databases.

## Additional requirements

The package is using SQLAlchemy and depending on what database you want to connect to the installation of additional packages is required. Below are the instructions for the databases that are currently supported:

### Oracle
```
pip install cx_Oracle
```
### PostgreSQL
```
pip install psycopg2
```

### SQL Server (MSSQL)
```
pip install pyodbc
```

On Linux first follow the [Microsoft instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) to install the required drivers.

### MySQL
```
pip install pymysql
```