import sqlite3
import pandas as pd

DB_NAME = "parking_analysis.db"


def save_data(df, report):

    connection = sqlite3.connect(DB_NAME)

    df.to_sql(
        "parking_data",
        connection,
        if_exists="replace",
        index=False
    )

    report_df = pd.DataFrame(
        list(report.items()),
        columns=["Metric", "Value"]
    )

    report_df.to_sql(
        "quality_report",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()


def read_data(table_name):

    connection = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        connection
    )

    connection.close()

    return df