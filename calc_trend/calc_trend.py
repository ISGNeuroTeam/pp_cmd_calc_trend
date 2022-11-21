import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def calc_trend(
        df: pd.DataFrame,
        value_col: str,
        window: str = "1M") -> pd.DataFrame:

    trend_col = "trend"
    trend_upper_col = "trend_upper"
    trend_lower_col = "trend_lower"

    def _calc_global_trend(df: pd.DataFrame, value_col: str) -> np.array:
        X = np.arange(0, len(df.index)).reshape(-1, 1)
        y = df[value_col]
        linreg = LinearRegression().fit(X, y)
        return linreg.predict(X)

    if window is None:
        trend = _calc_global_trend(df, value_col)
        df[trend_col] = trend
        return df[[trend_col, ]]
    segments = (
        df
        .resample(f"{window}", origin="start").mean()
        .index
        .insert(0, df.index.min())
    )

    for i in range(len(segments) - 1):
        segment_slice = (df.index >= segments[i]) & (df.index <= segments[i + 1])
        segment_df = df.loc[segment_slice]
        if segment_df.shape[0] == 0:
            continue

        segment_trend = _calc_global_trend(segment_df, value_col)
        segment_std = segment_df[value_col].std()

        df.loc[segment_slice, trend_col] = segment_trend
        df.loc[segment_slice, trend_upper_col] = segment_trend + 1.5 * segment_std
        df.loc[segment_slice, trend_lower_col] = segment_trend - 1.5 * segment_std

    if trend_col not in df.columns:
        df[trend_col] = 0  # np.NAN

    return df[[trend_col, trend_upper_col, trend_lower_col]]
