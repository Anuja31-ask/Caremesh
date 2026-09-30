"""
CareMesh - Synthetic Healthcare Network Data Generator

Purpose:
    Generate realistic synthetic healthcare operational data
    for the CareMesh prototype.

Generated datasets:
    1. facilities.csv
    2. daily_operations.csv
    3. inventory.csv

The data is SYNTHETIC and is intended only for prototype/demo use.
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42

NUM_FACILITIES = 30
NUM_DAYS = 180

OUTPUT_DIR = "data"

START_DATE = datetime(2026, 4, 1)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("CAREMesh - Synthetic Healthcare Data Generator")
print("=" * 70)

print(f"\nNumber of facilities : {NUM_FACILITIES}")
print(f"Number of days       : {NUM_DAYS}")
print(f"Output directory     : {OUTPUT_DIR}")


# ============================================================
# HEALTHCARE NETWORK
# ============================================================

# NOTE:
# These are synthetic prototype locations.
# They are NOT claiming to represent actual government facility data.

locations = [
    {
        "state": "Maharashtra",
        "district": "Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
    },
    {
        "state": "Maharashtra",
        "district": "Nashik",
        "latitude": 20.0059,
        "longitude": 73.7910,
    },
    {
        "state": "Maharashtra",
        "district": "Satara",
        "latitude": 17.6805,
        "longitude": 74.0183,
    },
    {
        "state": "Maharashtra",
        "district": "Nagpur",
        "latitude": 21.1458,
        "longitude": 79.0882,
    },
    {
        "state": "Maharashtra",
        "district": "Kolhapur",
        "latitude": 16.7050,
        "longitude": 74.2433,
    },
    {
        "state": "Maharashtra",
        "district": "Ahmednagar",
        "latitude": 19.0952,
        "longitude": 74.7496,
    },
    {
        "state": "Karnataka",
        "district": "Bengaluru",
        "latitude": 12.9716,
        "longitude": 77.5946,
    },
    {
        "state": "Karnataka",
        "district": "Mysuru",
        "latitude": 12.2958,
        "longitude": 76.6394,
    },
    {
        "state": "Karnataka",
        "district": "Mangaluru",
        "latitude": 12.9141,
        "longitude": 74.8560,
    },
    {
        "state": "Karnataka",
        "district": "Hubballi",
        "latitude": 15.3647,
        "longitude": 75.1240,
    },
    {
        "state": "Gujarat",
        "district": "Ahmedabad",
        "latitude": 23.0225,
        "longitude": 72.5714,
    },
    {
        "state": "Gujarat",
        "district": "Surat",
        "latitude": 21.1702,
        "longitude": 72.8311,
    },
    {
        "state": "Gujarat",
        "district": "Vadodara",
        "latitude": 22.3072,
        "longitude": 73.1812,
    },
    {
        "state": "Gujarat",
        "district": "Rajkot",
        "latitude": 22.3039,
        "longitude": 70.8022,
    },
    {
        "state": "Gujarat",
        "district": "Bhavnagar",
        "latitude": 21.7645,
        "longitude": 72.1519,
    },
]


# ============================================================
# MEDICINE CATALOG
# ============================================================

medicines = [
    {
        "medicine": "Amoxicillin",
        "category": "Antibiotic",
        "base_daily_demand": 180,
        "critical_stock_days": 5,
    },
    {
        "medicine": "Insulin",
        "category": "Diabetes",
        "base_daily_demand": 90,
        "critical_stock_days": 7,
    },
    {
        "medicine": "ORS",
        "category": "Emergency",
        "base_daily_demand": 220,
        "critical_stock_days": 5,
    },
    {
        "medicine": "Salbutamol",
        "category": "Respiratory",
        "base_daily_demand": 120,
        "critical_stock_days": 6,
    },
    {
        "medicine": "Paracetamol",
        "category": "Analgesic",
        "base_daily_demand": 250,
        "critical_stock_days": 5,
    },
    {
        "medicine": "Ceftriaxone",
        "category": "Antibiotic",
        "base_daily_demand": 75,
        "critical_stock_days": 7,
    },
]


# ============================================================
# FACILITY GENERATION
# ============================================================

print("\n[1/4] Generating healthcare facilities...")

facility_rows = []

for facility_index in range(NUM_FACILITIES):

    location = random.choice(locations)

    facility_type = random.choice(
        [
            "Primary Health Centre",
            "Community Health Centre",
            "District Hospital",
        ]
    )

    if facility_type == "Primary Health Centre":
        beds = random.randint(20, 50)

    elif facility_type == "Community Health Centre":
        beds = random.randint(50, 120)

    else:
        beds = random.randint(150, 350)

    facility_id = f"FAC-{facility_index + 1:03d}"

    facility_rows.append(
        {
            "facility_id": facility_id,
            "facility_name": f"{location['district']} {facility_type}",
            "facility_type": facility_type,
            "state": location["state"],
            "district": location["district"],
            "latitude": location["latitude"]
            + np.random.uniform(-0.05, 0.05),
            "longitude": location["longitude"]
            + np.random.uniform(-0.05, 0.05),
            "bed_capacity": beds,
        }
    )


facilities_df = pd.DataFrame(facility_rows)

facilities_path = os.path.join(
    OUTPUT_DIR,
    "facilities.csv"
)

facilities_df.to_csv(
    facilities_path,
    index=False
)

print(f"   Created: {facilities_path}")
print(f"   Facilities: {len(facilities_df)}")


# ============================================================
# DAILY OPERATIONS
# ============================================================

print("\n[2/4] Generating daily healthcare operations...")

operation_rows = []

for _, facility in facilities_df.iterrows():

    # Base characteristics for each facility
    base_footfall = np.random.randint(80, 400)

    base_staff = np.random.randint(20, 100)

    for day_number in range(NUM_DAYS):

        current_date = START_DATE + timedelta(
            days=day_number
        )

        # ----------------------------------------------------
        # Weekly seasonality
        # ----------------------------------------------------

        weekday = current_date.weekday()

        if weekday >= 5:
            weekday_factor = 0.85
        else:
            weekday_factor = 1.0

        # ----------------------------------------------------
        # Long-term trend
        # ----------------------------------------------------

        trend_factor = 1 + (day_number / NUM_DAYS) * 0.08

        # ----------------------------------------------------
        # Random demand variation
        # ----------------------------------------------------

        noise = np.random.normal(0, 0.08)

        patient_footfall = (
            base_footfall
            * weekday_factor
            * trend_factor
            * (1 + noise)
        )

        patient_footfall = max(
            20,
            int(patient_footfall)
        )

        # ----------------------------------------------------
        # Occasionally create demand spikes
        # ----------------------------------------------------

        if random.random() < 0.025:

            spike_multiplier = random.uniform(
                1.3,
                1.8
            )

            patient_footfall = int(
                patient_footfall
                * spike_multiplier
            )

            anomaly_event = 1

        else:

            anomaly_event = 0

        # ----------------------------------------------------
        # Bed occupancy
        # ----------------------------------------------------

        occupancy_rate = (
            patient_footfall
            / max(facility["bed_capacity"], 1)
        )

        occupancy_rate = min(
            0.98,
            max(
                0.25,
                occupancy_rate
                + np.random.normal(0, 0.08)
            )
        )

        occupied_beds = int(
            facility["bed_capacity"]
            * occupancy_rate
        )

        # ----------------------------------------------------
        # Staff availability
        # ----------------------------------------------------

        staff_availability = np.random.normal(
            0.90,
            0.06
        )

        staff_availability = min(
            1.0,
            max(
                0.60,
                staff_availability
            )
        )

        available_staff = int(
            base_staff
            * staff_availability
        )

        # ----------------------------------------------------
        # Supplier delay
        # ----------------------------------------------------

        if random.random() < 0.08:

            supplier_delay_days = random.randint(
                1,
                5
            )

        else:

            supplier_delay_days = 0

        operation_rows.append(
            {
                "date": current_date.strftime(
                    "%Y-%m-%d"
                ),
                "facility_id": facility["facility_id"],
                "patient_footfall": patient_footfall,
                "bed_capacity": facility["bed_capacity"],
                "occupied_beds": occupied_beds,
                "bed_occupancy_rate": round(
                    occupancy_rate,
                    3
                ),
                "staff_available": available_staff,
                "staff_availability_rate": round(
                    staff_availability,
                    3
                ),
                "supplier_delay_days": supplier_delay_days,
                "anomaly_event": anomaly_event,
            }
        )


operations_df = pd.DataFrame(
    operation_rows
)

operations_path = os.path.join(
    OUTPUT_DIR,
    "daily_operations.csv"
)

operations_df.to_csv(
    operations_path,
    index=False
)

print(
    f"   Created: {operations_path}"
)

print(
    f"   Records: {len(operations_df):,}"
)


# ============================================================
# MEDICINE INVENTORY + DEMAND
# ============================================================

print("\n[3/4] Generating medicine inventory data...")

inventory_rows = []

for _, facility in facilities_df.iterrows():

    for medicine in medicines:

        # Facility-specific demand scale
        facility_scale = np.random.uniform(
            0.7,
            1.4
        )

        base_demand = (
            medicine["base_daily_demand"]
            * facility_scale
        )

        # Initial inventory:
        # between approximately 10 and 30 days
        # of expected demand.

        initial_stock = int(
            base_demand
            * np.random.uniform(
                10,
                30
            )
        )

        current_inventory = initial_stock

        for day_number in range(NUM_DAYS):

            current_date = START_DATE + timedelta(
                days=day_number
            )

            # ------------------------------------------------
            # Match operations data
            # ------------------------------------------------

            operation = operations_df[
                (
                    operations_df["facility_id"]
                    == facility["facility_id"]
                )
                &
                (
                    operations_df["date"]
                    == current_date.strftime(
                        "%Y-%m-%d"
                    )
                )
            ].iloc[0]

            # ------------------------------------------------
            # Patient demand effect
            # ------------------------------------------------

            patient_factor = (
                operation["patient_footfall"]
                / 200
            )

            # ------------------------------------------------
            # Demand noise
            # ------------------------------------------------

            demand_noise = np.random.normal(
                1.0,
                0.10
            )

            daily_demand = (
                base_demand
                * patient_factor
                * demand_noise
            )

            # ------------------------------------------------
            # Anomaly / surge effect
            # ------------------------------------------------

            if operation["anomaly_event"] == 1:

                daily_demand *= np.random.uniform(
                    1.2,
                    1.5
                )

            daily_demand = max(
                1,
                int(daily_demand)
            )

            # ------------------------------------------------
            # Supplier replenishment
            # ------------------------------------------------

            reorder_point = (
                base_demand
                * medicine["critical_stock_days"]
            )

            if current_inventory < reorder_point:

                # Supplier delivery may be delayed
                if operation["supplier_delay_days"] == 0:

                    replenishment = int(
                        base_demand
                        * np.random.uniform(
                            8,
                            15
                        )
                    )

                else:

                    replenishment = 0

            else:

                replenishment = 0

            # ------------------------------------------------
            # Inventory update
            # ------------------------------------------------

            beginning_inventory = current_inventory

            current_inventory = (
                current_inventory
                - daily_demand
                + replenishment
            )

            current_inventory = max(
                0,
                int(current_inventory)
            )

            # ------------------------------------------------
            # Stock-out
            # ------------------------------------------------

            stockout = int(
                current_inventory <= 0
            )

            # ------------------------------------------------
            # Days of inventory remaining
            # ------------------------------------------------

            if daily_demand > 0:

                days_remaining = (
                    current_inventory
                    / daily_demand
                )

            else:

                days_remaining = 999

            inventory_rows.append(
                {
                    "date": current_date.strftime(
                        "%Y-%m-%d"
                    ),
                    "facility_id": facility["facility_id"],
                    "medicine": medicine["medicine"],
                    "medicine_category": medicine["category"],
                    "beginning_inventory": beginning_inventory,
                    "daily_demand": daily_demand,
                    "replenishment": replenishment,
                    "ending_inventory": current_inventory,
                    "days_of_inventory_remaining": round(
                        days_remaining,
                        2
                    ),
                    "supplier_delay_days": operation[
                        "supplier_delay_days"
                    ],
                    "stockout": stockout,
                }
            )


inventory_df = pd.DataFrame(
    inventory_rows
)

inventory_path = os.path.join(
    OUTPUT_DIR,
    "inventory.csv"
)

inventory_df.to_csv(
    inventory_path,
    index=False
)

print(
    f"   Created: {inventory_path}"
)

print(
    f"   Records: {len(inventory_df):,}"
)


# ============================================================
# DATA QUALITY CHECK
# ============================================================

print("\n[4/4] Running data quality checks...")

print("\nFacilities dataset:")
print(facilities_df.head(3))

print("\nOperations dataset:")
print(operations_df.head(3))

print("\nInventory dataset:")
print(inventory_df.head(3))


# Missing values

print("\nMissing values:")

print(
    "Facilities:",
    facilities_df.isnull().sum().sum()
)

print(
    "Operations:",
    operations_df.isnull().sum().sum()
)

print(
    "Inventory:",
    inventory_df.isnull().sum().sum()
)


# Stock-out statistics

stockout_count = inventory_df[
    "stockout"
].sum()

total_inventory_records = len(
    inventory_df
)

stockout_percentage = (
    stockout_count
    / total_inventory_records
) * 100


print("\nStock-out statistics:")

print(
    f"Total inventory records : "
    f"{total_inventory_records:,}"
)

print(
    f"Stock-out records       : "
    f"{stockout_count:,}"
)

print(
    f"Stock-out percentage    : "
    f"{stockout_percentage:.2f}%"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)

print("DATA GENERATION COMPLETE!")

print("=" * 70)

print("\nGenerated files:")

print(f"1. {facilities_path}")
print(f"2. {operations_path}")
print(f"3. {inventory_path}")

print("\nTotal records:")

print(
    f"Facilities : {len(facilities_df):,}"
)

print(
    f"Operations : {len(operations_df):,}"
)

print(
    f"Inventory  : {len(inventory_df):,}"
)

print("\nThese datasets are SYNTHETIC prototype data.")

print("\nNext step:")
print("Build the AI demand forecasting + stock-out risk engine.")