import os
import json
import pandas as pd

from data_cleaning import clean_parking_data
from analysis import parking_analysis
from database import save_data


DATA_FOLDER = "data"
OUTPUT_FOLDER = "outputs"

PARKING_FILE = os.path.join(
    DATA_FOLDER, "parking_data.csv"
)

EVENT_FILE = os.path.join(
    DATA_FOLDER, "event_calendar.csv"
)


def create_demo_dataset():

    records = [
        ["CarPark_A", 500, 250, "2016-10-01 08:00:00"],
        ["CarPark_A", 500, 400, "2016-10-01 10:00:00"],
        ["CarPark_A", 500, 450, "2016-10-01 12:00:00"],
        ["CarPark_A", 500, 300, "2016-10-02 08:00:00"],
        ["CarPark_A", 500, 350, "2016-10-02 10:00:00"],
        ["CarPark_B", 300, 100, "2016-10-01 08:00:00"],
        ["CarPark_B", 300, 200, "2016-10-01 10:00:00"],
        ["CarPark_B", 300, 250, "2016-10-01 12:00:00"],
        ["CarPark_B", 300, 150, "2016-10-02 08:00:00"],
        ["CarPark_B", 300, 180, "2016-10-02 10:00:00"]
    ]

    columns = [
        "SystemCodeNumber",
        "Capacity",
        "Occupancy",
        "LastUpdated"
    ]

    df = pd.DataFrame(records, columns=columns)

    df.to_csv(PARKING_FILE, index=False)

    print("Demo dataset created.")


def run_project():

    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if not os.path.exists(PARKING_FILE):
        create_demo_dataset()

    if not os.path.exists(EVENT_FILE):
        pd.DataFrame(
            columns=["Date", "Event_Name"]
        ).to_csv(EVENT_FILE, index=False)

    print("\nStarting Parking Data Pipeline...")

    # DATA CLEANING
    df, quality_report = clean_parking_data(
        PARKING_FILE
    )

    # DATA QUALITY REPORT
    print("\n========== DATA QUALITY REPORT ==========")

    for key, value in quality_report.items():
        print(f"{key}: {value}")

    print("=========================================")

    # EVENT DATA
    events = pd.read_csv(EVENT_FILE)

    if not events.empty:

        events["Date"] = pd.to_datetime(
            events["Date"],
            errors="coerce"
        ).dt.date.astype(str)

        event_dates = events["Date"].dropna().unique()

        df["is_event_day"] = df["Date"].isin(event_dates)

    else:
        df["is_event_day"] = False

    # DATA ANALYSIS
    results = parking_analysis(df)

    # DATABASE STORAGE
    save_data(df, quality_report)

    # SAVE CLEANED DATA
    df.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "cleaned_parking_data.csv"
        ),
        index=False
    )

    # SAVE PARKING SUMMARY
    results["parking_summary"].to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "parking_summary.csv"
        ),
        index=False
    )

    # SAVE HOURLY SUMMARY
    results["hourly_summary"].to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "hourly_summary.csv"
        ),
        index=False
    )

    # SAVE EVENT SUMMARY
    results["event_summary"].to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "event_summary.csv"
        ),
        index=False
    )

    # SAVE QUALITY REPORT
    with open(
        os.path.join(
            OUTPUT_FOLDER,
            "quality_report.json"
        ),
        "w"
    ) as file:

        json.dump(
            quality_report,
            file,
            indent=4
        )

    # FINAL RESULTS
    print("\n========== PROJECT RESULTS ==========")

    print("Project completed successfully!")

    print(
        "Total Records:",
        results["total_records"]
    )

    print(
        "Parking Areas:",
        results["total_parking_areas"]
    )

    print(
        "Average Occupancy:",
        results["average_occupancy"],
        "%"
    )

    print("======================================")


if __name__ == "__main__":
    run_project()