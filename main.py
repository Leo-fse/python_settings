import random
from datetime import timedelta

import numpy as np
import pandas as pd

pd.set_option("display.max_rows", 1000)


def generate_dummy_data() -> pd.DataFrame:
    """
    ダミーデータを生成する関数。

    Returns:
        pd.DataFrame: ダミーデータが格納されたDataFrame。
    """
    date_index = pd.date_range(start="2023-01-01", end="2023-01-05", freq="s")

    columns = ["data1", "data2", "data3"]
    data = {}
    for col in columns:
        data.update({col: np.random.randn(len(date_index))})
    df = pd.DataFrame(index=date_index, data=data)
    df["time_delta"] = [timedelta(seconds=random.randrange(1, 10)) for _ in range(len(df))]
    df["time_delta_cumsum"] = df["time_delta"].cumsum()
    df["DateTime"] = df.index + df["time_delta_cumsum"]
    df.drop(["time_delta", "time_delta_cumsum"], axis=1, inplace=True)
    # df["time_delta"] = df["time_delta"].dt.seconds
    df.set_index("DateTime", inplace=True)

    return df


def resample_dataframe(dataframe: pd.DataFrame, interval: str = "30s") -> pd.DataFrame:
    """
    DataFrameを指定されたインターバルでリサンプリングする関数。

    Parameters:
        dataframe (pd.DataFrame): リサンプリング対象のDataFrame。
        interval (str, optional): リサンプリングするインターバル。デフォルトは"30s"。

    Returns:
        pd.DataFrame: リサンプリングされたDataFrame。
    """
    re_index = pd.date_range(start=dataframe.index.min(), end=dataframe.index.max(), freq=interval)
    re_df = pd.DataFrame(index=re_index)
    result = pd.merge_asof(
        re_df,
        dataframe,
        left_index=True,
        right_index=True,
        direction="backward",
        tolerance=pd.Timedelta(seconds=15),
    )
    return result


if __name__ == "__main__":
    df = generate_dummy_data()
    print(df.head(50))
    print(resample_dataframe(df).head(50))
