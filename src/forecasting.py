"""
forecasting.py

Forecasting functions for the
AI Business Intelligence Dashboard.
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ============================================================
# TIME SERIES VALIDATION SPLIT
# ============================================================

def time_series_split(
    df,
    validation_ratio=0.2,
    date_column="date",
    target_column="revenue"
):
    """
    Split chronological data into training and validation sets.

    The data is NOT randomly shuffled because time-series
    forecasting must preserve chronological order.
    """

    data = validate_forecast_data(
        df,
        date_column,
        target_column
    )

    if len(data) < 10:
        raise ValueError(
            "At least 10 observations are required "
            "for time-series validation."
        )

    if not 0 < validation_ratio < 1:
        raise ValueError(
            "validation_ratio must be between 0 and 1."
        )

    split_index = int(
        len(data) * (1 - validation_ratio)
    )

    if split_index < 5:
        raise ValueError(
            "Training dataset is too small."
        )

    train_df = data.iloc[
        :split_index
    ].copy()

    validation_df = data.iloc[
        split_index:
    ].copy()

    return train_df, validation_df

# ============================================================
# LINEAR REGRESSION FORECAST
# ============================================================

def linear_regression_forecast(
    df,
    periods=30,
    date_column="date",
    target_column="revenue"
):
    """
    Forecast future revenue using Linear Regression.

    Time index is used as the independent variable.
    """

    data = validate_forecast_data(
        df,
        date_column,
        target_column
    )

    if len(data) < 5:
        raise ValueError(
            "At least 5 observations are required "
            "for linear regression forecasting."
        )

    data = data.reset_index(
        drop=True
    )

    X = np.arange(
        len(data)
    ).reshape(-1, 1)

    y = data[
        target_column
    ].values

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    future_X = np.arange(
        len(data),
        len(data) + periods
    ).reshape(-1, 1)

    predictions = model.predict(
        future_X
    )

    predictions = np.maximum(
        predictions,
        0
    )

    last_date = data[
        date_column
    ].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=periods,
        freq="D"
    )

    forecast_df = pd.DataFrame(
        {
            "date": future_dates,
            "forecast": predictions
        }
    )

    return forecast_df, model

# ============================================================
# LINEAR REGRESSION VALIDATION
# ============================================================

def validate_linear_regression(
    df,
    validation_ratio=0.2,
    date_column="date",
    target_column="revenue"
):
    """
    Train Linear Regression on historical training data
    and evaluate it on later unseen observations.
    """

    train_df, validation_df = time_series_split(
        df,
        validation_ratio,
        date_column,
        target_column
    )

    train_df = train_df.reset_index(
        drop=True
    )

    validation_df = validation_df.reset_index(
        drop=True
    )

    X_train = np.arange(
        len(train_df)
    ).reshape(-1, 1)

    y_train = train_df[
        target_column
    ].values

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    X_validation = np.arange(
        len(train_df),
        len(train_df) + len(validation_df)
    ).reshape(-1, 1)

    y_actual = validation_df[
        target_column
    ].values

    y_predicted = model.predict(
        X_validation
    )

    y_predicted = np.maximum(
        y_predicted,
        0
    )

    mae = mean_absolute_error(
        y_actual,
        y_predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_actual,
            y_predicted
        )
    )

    r2 = r2_score(
        y_actual,
        y_predicted
    )

    results = {
        "model": "Linear Regression",
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2)
    }

    validation_results = validation_df[
        [date_column, target_column]
    ].copy()

    validation_results[
        "prediction"
    ] = y_predicted

    return (
        results,
        validation_results,
        model
    )

# ============================================================
# MOVING AVERAGE VALIDATION
# ============================================================

def validate_moving_average(
    df,
    validation_ratio=0.2,
    window=7,
    date_column="date",
    target_column="revenue"
):
    """
    Evaluate the moving-average baseline against
    a chronological validation period.
    """

    train_df, validation_df = time_series_split(
        df,
        validation_ratio,
        date_column,
        target_column
    )

    if len(train_df) < window:
        raise ValueError(
            f"Training data must contain at least "
            f"{window} observations."
        )

    history = (
        train_df[target_column]
        .astype(float)
        .tolist()
    )

    predictions = []

    for actual_value in validation_df[
        target_column
    ]:

        recent_values = history[
            -window:
        ]

        prediction = np.mean(
            recent_values
        )

        prediction = max(
            0,
            float(prediction)
        )

        predictions.append(
            prediction
        )

        # For validation, use the ACTUAL observed value
        # when moving to the next prediction.
        history.append(
            float(actual_value)
        )

    y_actual = validation_df[
        target_column
    ].values

    y_predicted = np.array(
        predictions
    )

    mae = mean_absolute_error(
        y_actual,
        y_predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_actual,
            y_predicted
        )
    )

    r2 = r2_score(
        y_actual,
        y_predicted
    )

    results = {
        "model": "7-Day Moving Average",
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2)
    }

    validation_results = validation_df[
        [date_column, target_column]
    ].copy()

    validation_results[
        "prediction"
    ] = y_predicted

    return (
        results,
        validation_results
    )

# ============================================================
# MODEL COMPARISON
# ============================================================

def compare_forecasting_models(
    df,
    validation_ratio=0.2,
    window=7,
    date_column="date",
    target_column="revenue"
):
    """
    Compare the moving-average baseline and
    linear regression using chronological validation.
    """

    moving_average_results, moving_average_validation = (
        validate_moving_average(
            df,
            validation_ratio,
            window,
            date_column,
            target_column
        )
    )

    linear_results, linear_validation, linear_model = (
        validate_linear_regression(
            df,
            validation_ratio,
            date_column,
            target_column
        )
    )

    comparison = pd.DataFrame(
        [
            moving_average_results,
            linear_results
        ]
    )

    # Lower RMSE is preferred.
    best_model = comparison.loc[
        comparison["rmse"].idxmin(),
        "model"
    ]

    return {
        "comparison": comparison,
        "best_model": best_model,
        "moving_average_validation":
            moving_average_validation,
        "linear_validation":
            linear_validation,
        "linear_model":
            linear_model
    }


# ============================================================
# VALIDATE FORECAST INPUT
# ============================================================

def validate_forecast_data(
    df,
    date_column="date",
    target_column="revenue"
):
    """
    Validate the dataframe before forecasting.
    """

    if df is None:
        raise ValueError(
            "Forecasting dataframe cannot be None."
        )

    if df.empty:
        raise ValueError(
            "Forecasting dataframe is empty."
        )

    required_columns = [
        date_column,
        target_column
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    data = df[
        [date_column, target_column]
    ].copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    data[target_column] = pd.to_numeric(
        data[target_column],
        errors="coerce"
    )

    data = data.dropna(
        subset=[
            date_column,
            target_column
        ]
    )

    data = data.sort_values(
        date_column
    )

    return data


# ============================================================
# MOVING AVERAGE FORECAST
# ============================================================

def moving_average_forecast(
    df,
    periods=30,
    window=7,
    date_column="date",
    target_column="revenue"
):
    """
    Forecast future values using a rolling moving average.

    The forecast is recursive:
    each new prediction becomes part of the
    window used for the following prediction.
    """

    data = validate_forecast_data(
        df,
        date_column,
        target_column
    )

    if len(data) < window:
        raise ValueError(
            f"At least {window} historical observations "
            f"are required."
        )

    historical_values = (
        data[target_column]
        .astype(float)
        .tolist()
    )

    last_date = data[date_column].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=periods,
        freq="D"
    )

    predictions = []

    values = historical_values.copy()

    for _ in range(periods):

        recent_values = values[-window:]

        prediction = np.mean(
            recent_values
        )

        prediction = max(
            0,
            float(prediction)
        )

        predictions.append(
            prediction
        )

        values.append(
            prediction
        )

    forecast_df = pd.DataFrame(
        {
            "date": future_dates,
            "forecast": predictions
        }
    )

    return forecast_df


# ============================================================
# HISTORICAL + FORECAST DATA
# ============================================================

def create_forecast_dataset(
    df,
    forecast_df,
    date_column="date",
    target_column="revenue"
):
    """
    Combine historical revenue and future forecast
    into one dataframe.
    """

    historical = validate_forecast_data(
        df,
        date_column,
        target_column
    )

    historical = historical.rename(
        columns={
            target_column: "actual"
        }
    )

    historical["forecast"] = np.nan

    combined = pd.concat(
        [
            historical[
                [
                    date_column,
                    "actual",
                    "forecast"
                ]
            ],
            forecast_df[
                [
                    date_column,
                    "forecast"
                ]
            ].assign(
                actual=np.nan
            )[
                [
                    date_column,
                    "actual",
                    "forecast"
                ]
            ]
        ],
        ignore_index=True
    )

    combined = combined.sort_values(
        date_column
    )

    return combined.reset_index(
        drop=True
    )


# ============================================================
# FORECAST SUMMARY
# ============================================================

def forecast_summary(
    forecast_df
):
    """
    Generate basic summary statistics
    for the forecast period.
    """

    if forecast_df.empty:
        raise ValueError(
            "Forecast dataframe is empty."
        )

    total_forecast = (
        forecast_df["forecast"].sum()
    )

    average_forecast = (
        forecast_df["forecast"].mean()
    )

    minimum_forecast = (
        forecast_df["forecast"].min()
    )

    maximum_forecast = (
        forecast_df["forecast"].max()
    )

    return {
        "total_forecast": float(
            total_forecast
        ),
        "average_daily_forecast": float(
            average_forecast
        ),
        "minimum_daily_forecast": float(
            minimum_forecast
        ),
        "maximum_daily_forecast": float(
            maximum_forecast
        )
    }

# ============================================================
# FINAL MODEL SELECTION + FORECAST
# ============================================================

def generate_best_forecast(
    df,
    periods=30,
    validation_ratio=0.2,
    window=7,
    date_column="date",
    target_column="revenue"
):
    """
    Compare forecasting models, select the best model,
    retrain the selected approach using all available
    historical data, and generate the final forecast.
    """

    data = validate_forecast_data(
        df,
        date_column,
        target_column
    )

    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    model_results = compare_forecasting_models(
        data,
        validation_ratio=validation_ratio,
        window=window,
        date_column=date_column,
        target_column=target_column
    )

    comparison = model_results[
        "comparison"
    ]

    best_model = model_results[
        "best_model"
    ]

    # --------------------------------------------------------
    # GENERATE FINAL FORECAST
    # --------------------------------------------------------

    if best_model == "7-Day Moving Average":

        forecast_df = moving_average_forecast(
            data,
            periods=periods,
            window=window,
            date_column=date_column,
            target_column=target_column
        )

    elif best_model == "Linear Regression":

        forecast_df, _ = linear_regression_forecast(
            data,
            periods=periods,
            date_column=date_column,
            target_column=target_column
        )

    else:

        raise ValueError(
            f"Unknown forecasting model: {best_model}"
        )

    # --------------------------------------------------------
    # COMBINE HISTORICAL + FORECAST
    # --------------------------------------------------------

    combined_df = create_forecast_dataset(
        data,
        forecast_df,
        date_column=date_column,
        target_column=target_column
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = forecast_summary(
        forecast_df
    )

    return {
        "best_model": best_model,
        "comparison": comparison,
        "forecast": forecast_df,
        "combined": combined_df,
        "summary": summary
    }

