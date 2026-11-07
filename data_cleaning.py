import pandas as pd


def clean_parking_data(file_path):
    df = pd.read_csv(file_path)

    # Standardize column names
    df.columns = df.columns.str.strip()

    required = [
        "SystemCodeNumber",
        "Capacity",
        "Occupancy",
        "LastUpdated"
    ]

    missing_columns = [
        col for col in required if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    before = len(df)
    missing_before = int(df.isnull().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    # Remove duplicate records
    df = df.drop_duplicates()

    # Clean parking names
    df["SystemCodeNumber"] = (
        df["SystemCodeNumber"].astype(str).str.strip()
    )

    # Convert numeric columns
    df["Capacity"] = pd.to_numeric(
        df["Capacity"], errors="coerce"
    )

    df["Occupancy"] = pd.to_numeric(
        df["Occupancy"], errors="coerce"
    )

    # Convert date and time
    df["LastUpdated"] = pd.to_datetime(
        df["LastUpdated"], errors="coerce"
    )

    # Remove missing values
    df = df.dropna(
        subset=[
            "SystemCodeNumber",
            "Capacity",
            "Occupancy",
            "LastUpdated"
        ]
    )

    # Remove invalid records
    df = df[
        (df["Capacity"] > 0) &
        (df["Occupancy"] >= 0) &
        (df["Occupancy"] <= df["Capacity"])
    ]

    # Create useful columns
    df["Date"] = df["LastUpdated"].dt.date.astype(str)
    df["Hour"] = df["LastUpdated"].dt.hour

    df["OccupancyRate"] = (
        df["Occupancy"] / df["Capacity"] * 100
    ).round(2)

    df = df.reset_index(drop=True)

    report = {
        "records_before": before,
        "records_after": len(df),
        "missing_values_before": missing_before,
        "duplicates_before": duplicates_before,
        "records_removed": before - len(df),
        "missing_values_after": int(df.isnull().sum().sum()),
        "duplicates_after": int(df.duplicated().sum())
    }

    return df, report