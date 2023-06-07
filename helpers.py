from typing import List, Tuple

import numpy as np
import pandas as pd

import constants as c


def get_batch_mean_df(df: pd.DataFrame, batch_size: int) -> pd.DataFrame:
    mean_df = df[df[c.BATCH_INDEX_COLUMN] <= batch_size]
    mean_df = mean_df.groupby(np.arange(len(mean_df)) // batch_size).mean()

    for column in mean_df.columns:
        if column not in [
            c.BATCH_INDEX_COLUMN,
            c.MEASUREMENT_INDEX_COLUMN,
            c.ROOM_INDEX_COLUMN,
            c.X_COLUMN,
            c.Y_COLUMN,
            c.Z_COLUMN,
        ] and not column.startswith(c.UNNAMED_COLUMN):
            nan_value = -1
            mean_df[column] = mean_df[column].fillna(nan_value)
            mean_df[column] = mean_df[column].round()
            mean_df[column] = mean_df[column].astype(int)
            mean_df[column] = mean_df[column].astype(float)
            mean_df[column] = mean_df[column].replace(nan_value, np.nan)

    for column in mean_df.columns:
        if column == c.BATCH_INDEX_COLUMN or column.startswith(c.UNNAMED_COLUMN):
            mean_df = mean_df.drop(columns=[column])

    return mean_df


def get_df_with_specific_measurements(
    df: pd.DataFrame, specific_measurements: List[Tuple[int, int]]
) -> pd.DataFrame:
    # TODO: Write that Number of measurements to include, could have worked,
    #   but in this way the performance probably is better
    df_new = df
    for index, row in df_new.iterrows():
        include_measurement = False
        for room_and_measurement in specific_measurements:
            if (
                row[c.ROOM_INDEX_COLUMN] == room_and_measurement[0]
                and row[c.MEASUREMENT_INDEX_COLUMN] == room_and_measurement[1]
            ):
                include_measurement = True
        if not include_measurement:
            df_new.drop(index, inplace=True)
    return df_new
