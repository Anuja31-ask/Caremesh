"""
CareMesh - Healthcare Resilience Intelligence Engine

This module provides:

1. Medicine demand forecasting
2. Stock-out risk prediction
3. Facility resilience scoring
4. Explainable risk factors

All data used by the prototype is synthetic.
"""

import os
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score


warnings.filterwarnings("ignore")


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = "data"
MODEL_DIR = "models"

INVENTORY_FILE = os.path.join(
    DATA_DIR,
    "inventory.csv"
)

OPERATIONS_FILE = os.path.join(
    DATA_DIR,
    "daily_operations.csv"
)

FACILITIES_FILE = os.path.join(
    DATA_DIR,
    "facilities.csv"
)

DEMAND_MODEL_FILE = os.path.join(
    MODEL_DIR,
    "demand_model.joblib"
)

STOCKOUT_MODEL_FILE = os.path.join(
    MODEL_DIR,
    "stockout_model.joblib"
)


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("=" * 70)
    print("CAREMESH RESILIENCE ENGINE")
    print("=" * 70)

    print("\n[1/7] Loading datasets...")

    inventory = pd.read_csv(
        INVENTORY_FILE
    )

    operations = pd.read_csv(
        OPERATIONS_FILE
    )

    facilities = pd.read_csv(
        FACILITIES_FILE
    )

    inventory["date"] = pd.to_datetime(
        inventory["date"]
    )

    operations["date"] = pd.to_datetime(
        operations["date"]
    )

    print(
        f"   Inventory records : {len(inventory):,}"
    )

    print(
        f"   Operations records: {len(operations):,}"
    )

    print(
        f"   Facilities        : {len(facilities):,}"
    )

    return inventory, operations, facilities


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(inventory, operations):

    print("\n[2/7] Creating ML features...")

    # --------------------------------------------------------
    # Aggregate medicine demand at facility/day level
    # --------------------------------------------------------

    medicine_daily = (
        inventory
        .groupby(
            [
                "date",
                "facility_id"
            ],
            as_index=False
        )
        .agg(
            total_daily_demand=(
                "daily_demand",
                "sum"
            ),
            total_inventory=(
                "ending_inventory",
                "sum"
            ),
            stockout_count=(
                "stockout",
                "sum"
            ),
            avg_days_inventory=(
                "days_of_inventory_remaining",
                "mean"
            )
        )
    )

    # --------------------------------------------------------
    # Add operational information
    # --------------------------------------------------------

    data = medicine_daily.merge(
        operations,
        on=[
            "date",
            "facility_id"
        ],
        how="left"
    )

    # --------------------------------------------------------
    # Calendar features
    # --------------------------------------------------------

    data["day_of_week"] = (
        data["date"].dt.dayofweek
    )

    data["day_of_month"] = (
        data["date"].dt.day
    )

    data["month"] = (
        data["date"].dt.month
    )

    # --------------------------------------------------------
    # Lag features
    # --------------------------------------------------------

    data = data.sort_values(
        [
            "facility_id",
            "date"
        ]
    )

    grouped = data.groupby(
        "facility_id"
    )

    data["demand_lag_1"] = (
        grouped[
            "total_daily_demand"
        ]
        .shift(1)
    )

    data["demand_lag_7"] = (
        grouped[
            "total_daily_demand"
        ]
        .shift(7)
    )

    # --------------------------------------------------------
    # Rolling demand
    # --------------------------------------------------------

    data["demand_7day_avg"] = (
        grouped[
            "total_daily_demand"
        ]
        .transform(
            lambda x:
            x.rolling(
                7,
                min_periods=1
            ).mean()
        )
    )

    # --------------------------------------------------------
    # Fill missing lag values
    # --------------------------------------------------------

    data = data.fillna(0)

    print(
        f"   Feature records: {len(data):,}"
    )

    return data


# ============================================================
# DEMAND FORECAST MODEL
# ============================================================

def train_demand_model(data):

    print("\n[3/7] Training demand forecasting model...")

    features = [
        "patient_footfall",
        "bed_occupancy_rate",
        "staff_availability_rate",
        "supplier_delay_days",
        "day_of_week",
        "day_of_month",
        "month",
        "demand_lag_1",
        "demand_lag_7",
        "demand_7day_avg",
    ]

    target = "total_daily_demand"

    # --------------------------------------------------------
    # Remove early rows with insufficient history
    # --------------------------------------------------------

    model_data = data[
        data["date"]
        >= data["date"].min()
        + pd.Timedelta(days=7)
    ].copy()

    X = model_data[features]
    y = model_data[target]

    # --------------------------------------------------------
    # Time-based split
    # --------------------------------------------------------

    split_index = int(
        len(model_data) * 0.8
    )

    X_train = X.iloc[
        :split_index
    ]

    X_test = X.iloc[
        split_index:
    ]

    y_train = y.iloc[
        :split_index
    ]

    y_test = y.iloc[
        split_index:
    ]

    print(
        f"   Training records: {len(X_train):,}"
    )

    print(
        f"   Testing records : {len(X_test):,}"
    )

    # --------------------------------------------------------
    # Random Forest model
    # --------------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=120,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    print(
        f"   Demand MAE: {mae:.2f}"
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    joblib.dump(
        {
            "model": model,
            "features": features
        },
        DEMAND_MODEL_FILE
    )

    print(
        f"   Saved model: {DEMAND_MODEL_FILE}"
    )

    return model, features


# ============================================================
# STOCK-OUT RISK MODEL
# ============================================================

def train_stockout_model(data):

    print("\n[4/7] Training stock-out risk model...")

    # --------------------------------------------------------
    # Create future stock-out target
    # --------------------------------------------------------

    data = data.sort_values(
        [
            "facility_id",
            "date"
        ]
    ).copy()

    grouped = data.groupby(
        "facility_id"
    )

    # Look ahead seven days.
    #
    # If stock-out happens within the next seven days,
    # target = 1.

    future_stockout = (
        grouped["stockout_count"]
        .transform(
            lambda x:
            x.shift(-1)
            .rolling(
                7,
                min_periods=1
            )
            .max()
        )
    )

    data["future_stockout"] = (
        future_stockout
        .fillna(0)
        .astype(int)
    )

    features = [
        "total_inventory",
        "total_daily_demand",
        "avg_days_inventory",
        "patient_footfall",
        "bed_occupancy_rate",
        "staff_availability_rate",
        "supplier_delay_days",
        "demand_7day_avg",
    ]

    model_data = data[
        data["date"]
        < data["date"].max()
        - pd.Timedelta(days=7)
    ].copy()

    X = model_data[features]
    y = model_data["future_stockout"]

    # --------------------------------------------------------
    # Check target distribution
    # --------------------------------------------------------

    print("\n   Stock-out target distribution:")

    print(
        y.value_counts()
    )

    # --------------------------------------------------------
    # Time-based split
    # --------------------------------------------------------

    split_index = int(
        len(model_data) * 0.8
    )

    X_train = X.iloc[
        :split_index
    ]

    X_test = X.iloc[
        split_index:
    ]

    y_train = y.iloc[
        :split_index
    ]

    y_test = y.iloc[
        split_index:
    ]

    # --------------------------------------------------------
    # Classifier
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        f"\n   Stock-out accuracy: "
        f"{accuracy:.3f}"
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    joblib.dump(
        {
            "model": model,
            "features": features
        },
        STOCKOUT_MODEL_FILE
    )

    print(
        f"   Saved model: {STOCKOUT_MODEL_FILE}"
    )

    return model, features


# ============================================================
# FACILITY RESILIENCE SCORE
# ============================================================

def calculate_resilience_scores(
    inventory,
    operations,
    facilities
):

    print(
        "\n[5/7] Calculating facility resilience scores..."
    )

    # --------------------------------------------------------
    # Most recent operational information
    # --------------------------------------------------------

    latest_operation_date = (
        operations["date"].max()
    )

    latest_operations = operations[
        operations["date"]
        == latest_operation_date
    ].copy()

    # --------------------------------------------------------
    # Most recent inventory
    # --------------------------------------------------------

    latest_inventory_date = (
        inventory["date"].max()
    )

    latest_inventory = inventory[
        inventory["date"]
        == latest_inventory_date
    ].copy()

    # --------------------------------------------------------
    # Aggregate medicine information
    # --------------------------------------------------------

    inventory_summary = (
        latest_inventory
        .groupby(
            "facility_id",
            as_index=False
        )
        .agg(
            total_inventory=(
                "ending_inventory",
                "sum"
            ),
            avg_days_inventory=(
                "days_of_inventory_remaining",
                "mean"
            ),
            stockout_count=(
                "stockout",
                "sum"
            )
        )
    )

    # --------------------------------------------------------
    # Merge
    # --------------------------------------------------------

    scores = (
        facilities
        .merge(
            latest_operations,
            on="facility_id",
            how="left"
        )
        .merge(
            inventory_summary,
            on="facility_id",
            how="left"
        )
    )

    scores = scores.fillna(0)

    # --------------------------------------------------------
    # Convert metrics to risk scores
    #
    # Higher score = better resilience.
    # --------------------------------------------------------

    inventory_score = np.clip(
        scores["avg_days_inventory"]
        / 20
        * 100,
        0,
        100
    )

    demand_score = np.clip(
        100
        - scores["bed_occupancy_rate"]
        * 100,
        0,
        100
    )

    staff_score = np.clip(
        scores["staff_availability_rate"]
        * 100,
        0,
        100
    )

    supplier_score = np.clip(
        100
        - scores["supplier_delay_days"]
        * 20,
        0,
        100
    )

    stockout_score = np.clip(
        100
        - scores["stockout_count"]
        * 20,
        0,
        100
    )

    # --------------------------------------------------------
    # Weighted resilience score
    # --------------------------------------------------------

    scores["resilience_score"] = (
        inventory_score * 0.30
        + demand_score * 0.20
        + staff_score * 0.15
        + supplier_score * 0.15
        + stockout_score * 0.20
    )

    scores["resilience_score"] = (
        scores["resilience_score"]
        .round(1)
    )

    # --------------------------------------------------------
    # Risk classification
    # --------------------------------------------------------

    def classify_risk(score):

        if score < 40:
            return "CRITICAL"

        elif score < 60:
            return "HIGH"

        elif score < 80:
            return "MODERATE"

        else:
            return "LOW"

    scores["risk_level"] = (
        scores["resilience_score"]
        .apply(classify_risk)
    )

    print("\n   Risk distribution:")

    print(
        scores["risk_level"]
        .value_counts()
    )

    return scores


# ============================================================
# EXPLAINABLE RISK FACTORS
# ============================================================

def explain_facility_risk(
    facility_row
):

    reasons = []

    if facility_row[
        "avg_days_inventory"
    ] < 5:

        reasons.append(
            "Low medicine inventory"
        )

    if facility_row[
        "bed_occupancy_rate"
    ] > 0.85:

        reasons.append(
            "High bed occupancy"
        )

    if facility_row[
        "staff_availability_rate"
    ] < 0.80:

        reasons.append(
            "Reduced staff availability"
        )

    if facility_row[
        "supplier_delay_days"
    ] >= 3:

        reasons.append(
            "Supplier delay detected"
        )

    if facility_row[
        "stockout_count"
    ] > 0:

        reasons.append(
            "Existing medicine stock-out"
        )

    if not reasons:

        reasons.append(
            "No major operational risk detected"
        )

    return reasons


# ============================================================
# SAVE RESULTS
# ============================================================

def save_resilience_results(
    scores
):

    print(
        "\n[6/7] Saving resilience results..."
    )

    output_path = os.path.join(
        DATA_DIR,
        "facility_resilience.csv"
    )

    scores.to_csv(
        output_path,
        index=False
    )

    print(
        f"   Saved: {output_path}"
    )

    return output_path


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    # Load data

    inventory, operations, facilities = (
        load_data()
    )

    # Create features

    feature_data = create_features(
        inventory,
        operations
    )

    # Train demand model

    train_demand_model(
        feature_data
    )

    # Train stockout model

    train_stockout_model(
        feature_data
    )

    # Calculate resilience

    scores = calculate_resilience_scores(
        inventory,
        operations,
        facilities
    )

    # Add explanations

    print(
        "\n[7/7] Generating explainable risk factors..."
    )

    scores["risk_reasons"] = (
        scores.apply(
            explain_facility_risk,
            axis=1
        )
    )

    # Save

    save_resilience_results(
        scores
    )

    # --------------------------------------------------------
    # DISPLAY IMPORTANT FACILITIES
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "TOP HIGH-RISK FACILITIES"
    )

    print(
        "=" * 70
    )

    high_risk = (
        scores
        .sort_values(
            "resilience_score"
        )
        .head(10)
    )

    print(
        high_risk[
            [
                "facility_id",
                "facility_name",
                "district",
                "resilience_score",
                "risk_level",
                "avg_days_inventory",
                "bed_occupancy_rate",
                "supplier_delay_days",
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "RESILIENCE ENGINE COMPLETE"
    )

    print(
        "=" * 70
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()