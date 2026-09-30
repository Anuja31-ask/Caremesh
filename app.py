"""
CareMesh
Community Healthcare Resilience Intelligence

Prototype Command Center

IMPORTANT:
All healthcare data used in this prototype is synthetic.
It is intended for demonstration and hackathon purposes only.
"""

# ============================================================
# IMPORTS
# ============================================================

import os

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import folium

from streamlit_folium import st_folium


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareMesh | Healthcare Resilience",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ------------------------------------------------------
       GLOBAL
    ------------------------------------------------------ */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #F5FAF8 0%,
                #EDF7F4 45%,
                #F8FBFA 100%
            );
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* ------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------ */

    section[data-testid="stSidebar"] {
        background-color: #102A2A;
    }

    section[data-testid="stSidebar"] * {
        color: #E8F5F2;
    }


    /* ------------------------------------------------------
       HEADER
    ------------------------------------------------------ */

    .hero {
        background:
            linear-gradient(
                135deg,
                #123C3C,
                #1F6862
            );

        padding: 32px 38px;

        border-radius: 24px;

        color: white;

        margin-bottom: 25px;

        box-shadow:
            0px 12px 30px
            rgba(18, 60, 60, 0.15);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.85;
        margin-bottom: 18px;
    }

    .hero-badge {
        display: inline-block;

        padding: 7px 13px;

        border-radius: 20px;

        background: rgba(255,255,255,0.13);

        font-size: 13px;

        margin-right: 7px;
    }


    /* ------------------------------------------------------
       SECTION TITLES
    ------------------------------------------------------ */

    .section-title {
        font-size: 24px;

        font-weight: 750;

        color: #153B3B;

        margin-top: 25px;

        margin-bottom: 4px;
    }

    .section-subtitle {
        font-size: 14px;

        color: #647777;

        margin-bottom: 18px;
    }


    /* ------------------------------------------------------
       KPI CARDS
    ------------------------------------------------------ */

    .kpi-card {

        background: rgba(255,255,255,0.85);

        border: 1px solid #DDEBE7;

        border-radius: 18px;

        padding: 20px;

        min-height: 130px;

        box-shadow:
            0 5px 18px
            rgba(22, 71, 68, 0.06);
    }

    .kpi-label {

        font-size: 13px;

        color: #6A7E7D;

        margin-bottom: 8px;
    }

    .kpi-value {

        font-size: 31px;

        font-weight: 800;

        color: #153B3B;
    }

    .kpi-description {

        font-size: 12px;

        color: #718483;

        margin-top: 5px;
    }


    /* ------------------------------------------------------
       ALERT CARDS
    ------------------------------------------------------ */

    .alert-card {

        padding: 18px;

        border-radius: 16px;

        margin-bottom: 12px;

        background: #FFFFFF;

        border-left: 5px solid #D96C5F;

        box-shadow:
            0 4px 15px
            rgba(30, 70, 67, 0.06);
    }

    .alert-high {

        border-left-color: #E5A84B;

    }

    .alert-moderate {

        border-left-color: #6DA9A2;

    }

    .alert-title {

        font-weight: 750;

        color: #173C3B;

        font-size: 15px;

    }

    .alert-text {

        color: #647777;

        font-size: 13px;

        margin-top: 4px;

    }


    /* ------------------------------------------------------
       RESPONSE PANEL
    ------------------------------------------------------ */

    .response-panel {

        background:
            linear-gradient(
                135deg,
                #E5F3EF,
                #F4FAF8
            );

        border: 1px solid #CFE5DF;

        border-radius: 20px;

        padding: 25px;

        margin-top: 15px;
    }


    /* ------------------------------------------------------
       FOOTER
    ------------------------------------------------------ */

    .footer {

        text-align: center;

        color: #80908F;

        font-size: 12px;

        padding-top: 35px;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    facilities = pd.read_csv(
        "data/facilities.csv"
    )

    operations = pd.read_csv(
        "data/daily_operations.csv"
    )

    inventory = pd.read_csv(
        "data/inventory.csv"
    )

    resilience = pd.read_csv(
        "data/facility_resilience.csv"
    )

    operations["date"] = pd.to_datetime(
        operations["date"]
    )

    inventory["date"] = pd.to_datetime(
        inventory["date"]
    )

    return (
        facilities,
        operations,
        inventory,
        resilience
    )


# ============================================================
# LOAD DATA
# ============================================================

try:

    (
        facilities,
        operations,
        inventory,
        resilience
    ) = load_data()

except Exception as error:

    st.error(
        "Unable to load CareMesh data."
    )

    st.code(
        str(error)
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:800;
            margin-bottom:4px;
        ">
            🏥 CareMesh
        </div>

        <div style="
            font-size:12px;
            opacity:0.7;
            margin-bottom:25px;
        ">
            Healthcare Resilience Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Navigation"
    )

    page = st.radio(
        "Go to",
        [
            "Command Center",
            "Facility Intelligence",
            "Medicine Network",
            "Crisis Simulator"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        "### Network Filter"
    )

    states = sorted(
        facilities["state"]
        .unique()
        .tolist()
    )

    selected_state = st.selectbox(
        "State",
        ["All States"] + states
    )

    st.markdown("---")

    st.caption(
        "Prototype data is synthetic and "
        "intended for hackathon demonstration."
    )


# ============================================================
# FILTER DATA
# ============================================================

if selected_state != "All States":

    filtered_facilities = facilities[
        facilities["state"]
        == selected_state
    ].copy()

else:

    filtered_facilities = facilities.copy()


filtered_ids = filtered_facilities[
    "facility_id"
].tolist()


filtered_resilience = resilience[
    resilience["facility_id"]
    .isin(filtered_ids)
].copy()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            CareMesh
        </div>

        <div class="hero-subtitle">
            Community Healthcare Resilience Intelligence
        </div>

        <span class="hero-badge">
            ● AI-Powered
        </span>

        <span class="hero-badge">
            ● Predictive
        </span>

        <span class="hero-badge">
            ● Explainable
        </span>

        <span class="hero-badge">
            ● Response-Oriented
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.markdown(
        '<div class="section-title">'
        'Network Pulse'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'A live overview of healthcare network resilience.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_facilities = len(
        filtered_facilities
    )

    critical_count = len(
        filtered_resilience[
            filtered_resilience["risk_level"]
            == "CRITICAL"
        ]
    )

    high_count = len(
        filtered_resilience[
            filtered_resilience["risk_level"]
            == "HIGH"
        ]
    )

    average_resilience = (
        filtered_resilience[
            "resilience_score"
        ].mean()
    )

    latest_inventory = inventory[
        inventory["facility_id"]
        .isin(filtered_ids)
    ]

    latest_date = latest_inventory[
        "date"
    ].max()

    latest_inventory = latest_inventory[
        latest_inventory["date"]
        == latest_date
    ]

    stockout_count = int(
        latest_inventory[
            "stockout"
        ].sum()
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    HEALTHCARE FACILITIES
                </div>

                <div class="kpi-value">
                    {total_facilities}
                </div>

                <div class="kpi-description">
                    Facilities monitored
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    CRITICAL FACILITIES
                </div>

                <div class="kpi-value"
                     style="color:#C8564A;">
                    {critical_count}
                </div>

                <div class="kpi-description">
                    Immediate attention required
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    HIGH-RISK FACILITIES
                </div>

                <div class="kpi-value"
                     style="color:#C58A2C;">
                    {high_count}
                </div>

                <div class="kpi-description">
                    Emerging resilience concerns
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    NETWORK RESILIENCE
                </div>

                <div class="kpi-value">
                    {average_resilience:.1f}
                </div>

                <div class="kpi-description">
                    Average resilience score / 100
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # MAP + RISK DISTRIBUTION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Network Risk Map'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Geographic view of predicted healthcare vulnerability.'
        '</div>',
        unsafe_allow_html=True
    )

    map_col, chart_col = st.columns(
        [1.6, 1]
    )


    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    with map_col:

        center_lat = (
            filtered_facilities[
                "latitude"
            ].mean()
        )

        center_lon = (
            filtered_facilities[
                "longitude"
            ].mean()
        )

        network_map = folium.Map(
            location=[
                center_lat,
                center_lon
            ],
            zoom_start=6,
            tiles="CartoDB positron"
        )

        color_map = {
            "CRITICAL": "#D95D50",
            "HIGH": "#E4A84A",
            "MODERATE": "#6DA9A2",
            "LOW": "#4E8F83"
        }

        map_data = filtered_facilities.merge(
            filtered_resilience[
                [
                    "facility_id",
                    "resilience_score",
                    "risk_level"
                ]
            ],
            on="facility_id",
            how="left"
        )

        for _, row in map_data.iterrows():

            risk = row[
                "risk_level"
            ]

            popup_text = f"""
            <b>{row['facility_name']}</b><br>
            District: {row['district']}<br>
            Resilience Score:
            {row['resilience_score']:.1f}<br>
            Risk: {risk}
            """

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=9,
                color=color_map.get(
                    risk,
                    "#6DA9A2"
                ),
                fill=True,
                fill_color=color_map.get(
                    risk,
                    "#6DA9A2"
                ),
                fill_opacity=0.85,
                popup=folium.Popup(
                    popup_text,
                    max_width=300
                )
            ).add_to(
                network_map
            )

        st_folium(
            network_map,
            width=None,
            height=460
        )


    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    with chart_col:

        risk_counts = (
            filtered_resilience[
                "risk_level"
            ]
            .value_counts()
            .reindex(
                [
                    "CRITICAL",
                    "HIGH",
                    "MODERATE",
                    "LOW"
                ],
                fill_value=0
            )
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level",
            "Facilities"
        ]

        fig = px.bar(
            risk_counts,
            x="Risk Level",
            y="Facilities",
            text="Facilities",
            title="Facility Risk Distribution"
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#355454"
            ),
            height=400,
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )
        )

        fig.update_traces(
            marker_line_width=0
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # AI ALERT CENTER
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'AI Alert Center'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Priority signals identified by the resilience engine.'
        '</div>',
        unsafe_allow_html=True
    )

    alerts = (
        filtered_resilience
        .sort_values(
            "resilience_score"
        )
        .head(5)
    )

    for _, row in alerts.iterrows():

        reasons = []

        if row[
            "avg_days_inventory"
        ] < 5:

            reasons.append(
                "low medicine inventory"
            )

        if row[
            "bed_occupancy_rate"
        ] > 0.85:

            reasons.append(
                "high bed occupancy"
            )

        if row[
            "supplier_delay_days"
        ] >= 3:

            reasons.append(
                "supplier delay"
            )

        if row[
            "stockout_count"
        ] > 0:

            reasons.append(
                "medicine stock-out"
            )

        if not reasons:

            reasons.append(
                "multiple operational stress signals"
            )

        reason_text = ", ".join(
            reasons
        )

        risk = row[
            "risk_level"
        ]

        css_class = (
            "alert-card"
            if risk == "CRITICAL"
            else "alert-card alert-high"
        )

        icon = (
            "🔴"
            if risk == "CRITICAL"
            else "🟠"
        )

        st.markdown(
            f"""
            <div class="{css_class}">

                <div class="alert-title">
                    {icon}
                    {row['facility_name']}
                    · {risk}
                </div>

                <div class="alert-text">
                    Resilience score:
                    <b>{row['resilience_score']:.1f}</b>
                    &nbsp; • &nbsp;
                    Signals:
                    {reason_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FACILITY INTELLIGENCE
# ============================================================

elif page == "Facility Intelligence":

    st.markdown(
        '<div class="section-title">'
        'Facility Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Drill into the operational factors behind facility risk.'
        '</div>',
        unsafe_allow_html=True
    )

    facility_options = (
        filtered_facilities[
            "facility_id"
        ]
        .tolist()
    )

    selected_facility = st.selectbox(
        "Select facility",
        facility_options
    )

    facility = filtered_resilience[
        filtered_resilience[
            "facility_id"
        ]
        == selected_facility
    ].iloc[0]

    st.markdown(
        f"""
        <div class="response-panel">

            <h2 style="color:#153B3B;">
                {facility['facility_name']}
            </h2>

            <p style="color:#607574;">
                {facility['district']},
                {facility['state']}
                ·
                {facility['facility_type']}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Resilience Score",
            f"{facility['resilience_score']:.1f}/100"
        )

    with c2:

        st.metric(
            "Risk Level",
            facility["risk_level"]
        )

    with c3:

        st.metric(
            "Bed Occupancy",
            f"{facility['bed_occupancy_rate'] * 100:.1f}%"
        )

    with c4:

        st.metric(
            "Inventory Days",
            f"{facility['avg_days_inventory']:.1f}"
        )


    # --------------------------------------------------------
    # RISK FACTORS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Why is this facility at risk?'
        '</div>',
        unsafe_allow_html=True
    )

    reasons = []

    if facility[
        "avg_days_inventory"
    ] < 5:

        reasons.append(
            "📦 Medicine inventory is approaching a critical threshold."
        )

    if facility[
        "bed_occupancy_rate"
    ] > 0.85:

        reasons.append(
            "🛏️ Bed occupancy indicates elevated demand pressure."
        )

    if facility[
        "staff_availability_rate"
    ] < 0.80:

        reasons.append(
            "👩‍⚕️ Staff availability is below the preferred operating level."
        )

    if facility[
        "supplier_delay_days"
    ] >= 3:

        reasons.append(
            "🚚 Supplier delays may increase inventory risk."
        )

    if facility[
        "stockout_count"
    ] > 0:

        reasons.append(
            "⚠️ At least one medicine category is currently experiencing stock-out."
        )

    if not reasons:

        reasons.append(
            "✅ No major operational stress signal is currently detected."
        )

    for reason in reasons:

        st.info(
            reason
        )


    # --------------------------------------------------------
    # FACILITY OPERATIONS
    # --------------------------------------------------------

    facility_operations = operations[
        operations[
            "facility_id"
        ]
        == selected_facility
    ].copy()

    facility_operations = (
        facility_operations
        .sort_values("date")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=facility_operations["date"],
            y=facility_operations[
                "patient_footfall"
            ],
            mode="lines",
            name="Patient Footfall"
        )
    )

    fig.update_layout(
        title="Patient Demand Trend",
        xaxis_title="Date",
        yaxis_title="Patients",
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# MEDICINE NETWORK
# ============================================================

elif page == "Medicine Network":

    st.markdown(
        '<div class="section-title">'
        'Medicine Network'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Monitor medicine availability and emerging stock-out pressure.'
        '</div>',
        unsafe_allow_html=True
    )

    medicine_data = inventory[
        inventory["facility_id"]
        .isin(filtered_ids)
    ].copy()

    latest_date = medicine_data[
        "date"
    ].max()

    latest = medicine_data[
        medicine_data["date"]
        == latest_date
    ]

    medicine_summary = (
        latest
        .groupby(
            "medicine",
            as_index=False
        )
        .agg(
            inventory=(
                "ending_inventory",
                "sum"
            ),
            demand=(
                "daily_demand",
                "sum"
            ),
            avg_days_remaining=(
                "days_of_inventory_remaining",
                "mean"
            ),
            stockouts=(
                "stockout",
                "sum"
            )
        )
    )

    st.dataframe(
        medicine_summary,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # INVENTORY PRESSURE
    # --------------------------------------------------------

    fig = px.bar(
        medicine_summary,
        x="medicine",
        y="avg_days_remaining",
        title="Average Days of Medicine Inventory Remaining"
    )

    fig.add_hline(
        y=5,
        line_dash="dash",
        annotation_text="Critical threshold"
    )

    fig.update_layout(
        height=420,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CRISIS SIMULATOR
# ============================================================

elif page == "Crisis Simulator":

    st.markdown(
        '<div class="section-title">'
        'Crisis Simulator'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Explore how the healthcare network responds to sudden pressure.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="response-panel">

        <h3 style="color:#153B3B;">
        What happens if demand suddenly increases?
        </h3>

        <p style="color:#617573;">
        Simulate a demand surge and observe how facility
        resilience changes across the network.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    surge = st.slider(
        "Patient demand surge",
        min_value=0,
        max_value=100,
        value=25,
        step=5,
        format="%d%%"
    )

    # --------------------------------------------------------
    # SIMULATION
    # --------------------------------------------------------

    simulated = filtered_resilience.copy()

    demand_pressure = (
        simulated[
            "bed_occupancy_rate"
        ]
        + surge / 100
    )

    inventory_pressure = (
        simulated[
            "avg_days_inventory"
        ]
        - surge / 20
    )

    simulated["simulated_score"] = (
        simulated[
            "resilience_score"
        ]
        - demand_pressure * 15
        + inventory_pressure.clip(
            lower=0
        ) * 0.3
    )

    simulated[
        "simulated_score"
    ] = simulated[
        "simulated_score"
    ].clip(
        0,
        100
    )

    # --------------------------------------------------------
    # IMPACT
    # --------------------------------------------------------

    baseline_average = (
        filtered_resilience[
            "resilience_score"
        ].mean()
    )

    simulated_average = (
        simulated[
            "simulated_score"
        ].mean()
    )

    difference = (
        simulated_average
        - baseline_average
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Baseline Resilience",
            f"{baseline_average:.1f}"
        )

    with c2:

        st.metric(
            "Simulated Resilience",
            f"{simulated_average:.1f}"
        )

    with c3:

        st.metric(
            "Network Impact",
            f"{difference:.1f}",
            delta_color="inverse"
        )


    # --------------------------------------------------------
    # FACILITY IMPACT
    # --------------------------------------------------------

    comparison = simulated[
        [
            "facility_name",
            "resilience_score",
            "simulated_score"
        ]
    ].copy()

    comparison = comparison.sort_values(
        "simulated_score"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=comparison[
                "facility_name"
            ],
            x=comparison[
                "resilience_score"
            ],
            name="Baseline",
            orientation="h"
        )
    )

    fig.add_trace(
        go.Bar(
            y=comparison[
                "facility_name"
            ],
            x=comparison[
                "simulated_score"
            ],
            name="After Surge",
            orientation="h"
        )
    )

    fig.update_layout(
        title="Facility Resilience Under Demand Surge",
        barmode="group",
        height=650,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # RESPONSE RECOMMENDATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Recommended Response'
        '</div>',
        unsafe_allow_html=True
    )

    most_affected = comparison.head(
        min(5, len(comparison))
    )

    st.markdown(
        """
        <div class="response-panel">

        <h3 style="color:#153B3B;">
        Suggested resource prioritisation
        </h3>

        <p style="color:#617573;">
        Under the simulated demand surge, the following
        facilities should be reviewed first:
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    for _, row in most_affected.iterrows():

        st.warning(
            f"🏥 {row['facility_name']} — "
            f"simulated resilience "
            f"{row['simulated_score']:.1f}/100"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        CareMesh · Community Healthcare Resilience Intelligence

        <br>

        Prototype demonstration using synthetic data.

    </div>
    """,
    unsafe_allow_html=True
)