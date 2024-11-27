import datetime
import pandas as pd
from scibatt.config import COLUMN_NAMES, CURRENT_ZERO_TOLERANCE

def read_txt(filepath, raw = False):
    """
    Reads a maccor datafile and returns a dict of of dataframes;
    The key being the standard filename, and the dataframe being the data for each step in the programme
    """
    maccor_data_format = 2013 # The year of the format

    # This reads the csv file with some extra options
    with open(filepath, "r") as f:
        header_line_num = None
        for i, line in enumerate(f.readlines()):
            if line.startswith("Rec\tCycle"):
                header_line_num = i
                if "Cycle P" in line:
                    maccor_data_format = 2023
                break
        if not header_line_num:
            raise Exception(
                f"Could not find headerline in Maccor datafile: {filepath}"
            )  # TODO: Convert to custom exception

    cycle_col_name = "Cycle P" if maccor_data_format == 2023 else "Cycle"

    df = pd.read_csv(
        filepath,
        usecols=[cycle_col_name, "DPT Time", "Current", "Voltage", "Capacity", "Step", "MD"],
        encoding="UTF-8",
        header=header_line_num,
        delimiter="\t",
    )

    # Modifying time
    def convert_timestamp_to_unix_epoch(timestamp_str):
        try:
            timestamp_format = "%d.%m.%Y %H:%M:%S"
            datetime_obj = datetime.datetime.strptime(timestamp_str, timestamp_format)
        except:
            try:
                timestamp_format = "%d/%m/%Y %H:%M:%S"
                datetime_obj = datetime.datetime.strptime(timestamp_str, timestamp_format)
            except:
                try:
                    timestamp_format = "%m/%d/%Y %H:%M:%S"
                    datetime_obj = datetime.datetime.strptime(timestamp_str, timestamp_format)
                except Exception as e:
                    print(f"Cannot parse datetime format in maccor reader. Error: {e}")


        return datetime_obj.timestamp()  # Returns unix epoch float

    df[COLUMN_NAMES["TIME"]] = df["DPT Time"].apply(
        lambda x: convert_timestamp_to_unix_epoch(x)
    )

    # Making sure negative currents are negative
    df.loc[df["MD"] == "D", "Current"] *= -1

    # Rename columns to match spec
    df.rename(
        columns={
            "Current": COLUMN_NAMES["CURRENT"],
            "Voltage": COLUMN_NAMES["VOLTAGE1"],
            cycle_col_name: "Cycle",
        },
        inplace=True,
    )

    # TODO: This really does not fit into the system. The whole data storage system should be changed probably.
    # Was done to be able to get the raw data and print it.
    if raw:
        return df

    # Group by step to separate steps
    groups_step = df.groupby("Step")

    # Scan groups and add to return dict
    data = {}
    tol = CURRENT_ZERO_TOLERANCE
    for num, group_df in groups_step:
        mean_current = group_df[COLUMN_NAMES["CURRENT"]].mean()
        timestamp = group_df[COLUMN_NAMES["TIME"]].iloc[0]

        # Remove columns we don't want
        required_columns = [
            COLUMN_NAMES["TIME"],
            COLUMN_NAMES["CURRENT"],
            COLUMN_NAMES["VOLTAGE1"],
        ]
        group_df = group_df.drop(
            columns=[col for col in df if col not in required_columns]
        )

        if -tol < mean_current < tol:
            data[f"{timestamp}_cycling_p000.000A"] = group_df
        elif mean_current > tol:
            data[f"{timestamp}_cycling_p{mean_current:08.4f}A"] = group_df
        elif mean_current < tol:
            data[f"{timestamp}_cycling_n{mean_current:08.4f}A"] = group_df

    return data

def read_csv(filepath, raw = False):
    """
    Reads a maccor datafile exported using the MaccorExport2.exe, selecting CSV export, and the following columns: 
    Cycle P,Cycle C,Step,Test Time,Step Time,Capacity (AHr),Energy (WHr),Current (A),Voltage (V),MD,ES,DPT Time
    
    Returns a dict of of dataframes;
    The key being the standard filename, and the dataframe being the data for each step in the programme
    """
    # This reads the csv file with some extra options
    with open(filepath, "r") as f:
        header_line_num = None
        for i, line in enumerate(f.readlines()):
            if line.startswith("Rec,Cycle"):
                header_line_num = i
                break
        if not header_line_num:
            raise Exception(
                f"Could not find headerline in Maccor datafile: {filepath}"
            )  # TODO: Convert to custom exception

    df = pd.read_csv(
        filepath,
        usecols=["Cycle P", "DPT Time", "Current (A)", "Voltage (V)", "Capacity (AHr)", "Step", "MD"],
        encoding="UTF-8",
        header=header_line_num,
        delimiter=",",
    )

    # Modifying time
    format_string = "%m/%d/%Y %I:%M:%S %p"
    df['t'] = pd.to_datetime(df['DPT Time'], format='mixed')
    df['t'] = df['t'].apply(lambda x: x.timestamp())
    # df["t"] = df["DPT Time"].apply(lambda x: datetime.datetime.strptime(x, format_string).timestamp())

    # Making sure negative currents are negative
    df.loc[df["MD"] == "D", "Current (A)"] *= -1

    # Rename columns to match spec
    df.rename(
        columns={
            "Current (A)": COLUMN_NAMES["CURRENT"],
            "Voltage (V)": COLUMN_NAMES["VOLTAGE1"],
            "Cycle P": "Cycle",
        },
        inplace=True,
    )

    # TODO: This really does not fit into the system. The whole data storage system should be changed probably.
    # Was done to be able to get the raw data and print it.
    if raw:
        return df

    # Group by step to separate steps
    groups_step = df.groupby("Step")

    # Scan groups and add to return dict
    data = {}
    tol = CURRENT_ZERO_TOLERANCE
    for num, group_df in groups_step:
        mean_current = group_df[COLUMN_NAMES["CURRENT"]].mean()
        timestamp = group_df[COLUMN_NAMES["TIME"]].iloc[0]

        # Remove columns we don't want
        required_columns = [
            COLUMN_NAMES["TIME"],
            COLUMN_NAMES["CURRENT"],
            COLUMN_NAMES["VOLTAGE1"],
        ]
        group_df = group_df.drop(
            columns=[col for col in df if col not in required_columns]
        )

        if -tol < mean_current < tol:
            data[f"{timestamp}_cycling_p000.000A"] = group_df
        elif mean_current > tol:
            data[f"{timestamp}_cycling_p{mean_current:08.4f}A"] = group_df
        elif mean_current < tol:
            data[f"{timestamp}_cycling_n{mean_current:08.4f}A"] = group_df

    return data