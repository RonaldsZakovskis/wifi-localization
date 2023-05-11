from fingerprinting_based.data import gather_data, filter_columns


if __name__ == "__main__":  # If file is run directly
    df = gather_data(
        interface="wlp0s20f3",
        include_measurement_index=True,
        include_room_index=True,
        coordinate_dimensions=0
    )
    df.to_csv("wifi-localization-full.csv")

    columns_to_stay = [
        "measurement_index",
        "room_index"
    ]
    df_filtered = filter_columns(df, columns_to_stay)
    print(df_filtered)
    df.to_csv("wifi-localization-filtered.csv")

    columns_to_rename = {
        "measurement_index": "measurement",
        "room_index": "room"
    }
    df_renamed = df_filtered.rename(columns=columns_to_rename)
    print(df_renamed)
    df.to_csv("wifi-localization-renamed.csv")
