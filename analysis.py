import pandas as pd


def parking_analysis(df):

    total_records = len(df)

    total_parking_areas = df["SystemCodeNumber"].nunique()

    average_occupancy = round(
        df["OccupancyRate"].mean(), 2
    )

    total_capacity = int(df["Capacity"].sum())

    total_occupied = int(df["Occupancy"].sum())

    parking_summary = (
        df.groupby("SystemCodeNumber")
        .agg(
            Average_Occupancy=("OccupancyRate", "mean"),
            Maximum_Occupancy=("OccupancyRate", "max"),
            Total_Capacity=("Capacity", "max"),
            Average_Vehicles=("Occupancy", "mean")
        )
        .reset_index()
    )

    parking_summary["Average_Occupancy"] = (
        parking_summary["Average_Occupancy"].round(2)
    )

    hourly_summary = (
        df.groupby("Hour")
        .agg(
            Average_Occupancy=("OccupancyRate", "mean")
        )
        .reset_index()
    )

    event_summary = (
        df.groupby("is_event_day")
        .agg(
            Average_Occupancy=("OccupancyRate", "mean"),
            Total_Records=("OccupancyRate", "count")
        )
        .reset_index()
    )

    return {
        "total_records": total_records,
        "total_parking_areas": total_parking_areas,
        "average_occupancy": average_occupancy,
        "total_capacity": total_capacity,
        "total_occupied": total_occupied,
        "parking_summary": parking_summary,
        "hourly_summary": hourly_summary,
        "event_summary": event_summary
    }