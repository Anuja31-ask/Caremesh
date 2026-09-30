# CareMesh 🏥

### Community Healthcare Resilience Intelligence

> **From reactive healthcare response to proactive resilience intelligence.**

CareMesh is an AI-driven healthcare resilience and decision-support prototype designed to help identify vulnerabilities across interconnected healthcare facilities, monitor critical resources, explore disruption scenarios, and support proactive resource prioritisation.

The prototype provides a unified view of **facility resilience, patient demand, medicine availability, geographic risk, and crisis scenarios** through an interactive dashboard.

---

## 🚨 Problem

Healthcare systems operate as interconnected networks. A sudden change in patient demand, medicine availability, facility capacity, staffing, or supply conditions can create cascading pressure across multiple facilities.

Traditional monitoring can be heavily reactive:

```text
Crisis occurs
      ↓
Facility becomes overloaded
      ↓
Shortage is detected
      ↓
Resources are redistributed
      ↓
Response begins
```

This creates a need for tools that can help decision-makers **identify vulnerabilities earlier and explore potential scenarios before they become critical situations**.

---

## 💡 Our Solution

CareMesh provides a healthcare-network intelligence layer that combines operational indicators and scenario analysis into a single interactive platform.

```text
Healthcare Network Signals
        │
        ├── Patient Demand
        ├── Facility Capacity
        ├── Medicine Availability
        ├── Staffing
        └── Operational Conditions
                │
                ▼
        CAREMESH INTELLIGENCE
                │
        ├── Risk Assessment
        ├── Resilience Analysis
        ├── Network Visualisation
        └── Crisis Simulation
                │
                ▼
        DECISION SUPPORT
                │
        ├── Vulnerable Facilities
        ├── Early-Warning Insights
        └── Resource Prioritisation
```

The goal is to help healthcare stakeholders move from **reactive response** toward **proactive resilience planning**.

---

# ✨ Key Features

## 1. 📊 Command Center

The Command Center provides a network-level overview of healthcare resilience.

It provides visibility into:

* Facility-level risk
* Network resilience
* Critical and high-risk facilities
* Geographic risk distribution
* Early-warning insights
* Resource-prioritisation information

The objective is to give decision-makers a single place to understand the current state of the healthcare network.

---

## 2. 🏥 Facility Intelligence

CareMesh allows individual healthcare facilities to be examined in greater detail.

The prototype considers indicators such as:

* Patient demand
* Facility capacity
* Bed occupancy
* Staffing conditions
* Medicine availability
* Resilience-related indicators

This helps identify facilities that may require additional attention or resources.

---

## 3. 💊 Medicine Network

Medicine availability is an important component of healthcare resilience.

The Medicine Network module provides visibility into:

* Medicine inventory
* Facilities experiencing resource pressure
* Potential stock-out conditions
* Medicine availability across facilities
* Resource redistribution requirements

The goal is to encourage **proactive monitoring and planning rather than waiting for complete shortages to occur**.

---

## 4. 🚨 Crisis Simulator

The Crisis Simulator provides a "what-if" environment for exploring potential demand disruptions.

Users can simulate an increase in patient demand and observe how the healthcare network responds under the scenario.

The simulator demonstrates:

```text
Baseline Network
      ↓
Demand Surge
      ↓
Simulated Conditions
      ↓
Updated Resilience
      ↓
Affected Facilities
      ↓
Resource Prioritisation
```

This allows users to explore potential vulnerabilities before treating the scenario as an actual crisis.

> **Note:** The current simulator is a prototype scenario-analysis tool using synthetic data. It is not intended to predict real-world clinical outcomes.

---

## 🗺️ Geographic Risk Visualization

CareMesh includes an interactive geographic view of healthcare facilities.

The map helps users understand:

* Where facilities are located
* Which facilities are experiencing higher risk
* Geographic concentration of vulnerabilities
* Potential areas requiring resource attention

This provides a spatial perspective alongside the numerical resilience indicators.

---

# 🧠 Intelligence Layer

The current prototype combines operational indicators to generate facility and network-level resilience information.

The system considers factors such as:

```text
Patient Demand
      +
Facility Capacity
      +
Medicine Availability
      +
Operational Conditions
      ↓
Resilience / Risk Analysis
      ↓
Facility Prioritisation
```

The architecture is designed so that future versions can incorporate more advanced predictive machine-learning models and real-time healthcare data.

---

# 🛠️ Technology Stack

| Technology                    | Purpose                               |
| ----------------------------- | ------------------------------------- |
| **Python**                    | Core application and data processing  |
| **Streamlit**                 | Interactive web dashboard             |
| **Pandas**                    | Data processing and analysis          |
| **NumPy**                     | Numerical computation                 |
| **Plotly**                    | Interactive charts and visualisations |
| **Folium**                    | Geographic visualisation              |
| **Streamlit-Folium**          | Folium integration with Streamlit     |
| **Synthetic Healthcare Data** | Prototype demonstration               |

---

# 🏗️ Project Structure

```text
Caremesh/
│
├── app.py
├── data_generator.py
├── requirements.txt
│
├── data/
│   └── ...
│
├── assets/
│   └── ...
│
└── README.md
```

### Main files

**`app.py`**

Contains the Streamlit application, dashboard interface, visualisations, facility intelligence, medicine network, and crisis simulation.

**`data_generator.py`**

Generates the synthetic healthcare-network data used by the prototype.

**`requirements.txt`**

Contains the Python dependencies required to run the application.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

* Python 3.10+
* Git
* pip

---

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Caremesh
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open locally at:

```text
http://localhost:8501
```

---

# 📊 Data

The current prototype uses **synthetic healthcare-network data** created for demonstration and development purposes.

The synthetic data represents healthcare-network conditions such as:

* Facility characteristics
* Patient demand
* Capacity
* Medicine availability
* Staffing-related indicators
* Risk/resilience variables

### Why synthetic data?

The prototype is designed to demonstrate the architecture and decision-support workflow without using private or sensitive patient information.

Future versions can be designed to integrate appropriate real-world healthcare datasets while maintaining privacy, security, and regulatory requirements.

---

# 🔮 Future Roadmap

CareMesh is designed as a foundation that can evolve into a broader healthcare resilience platform.

### Phase 1 — Current Prototype

* Interactive healthcare dashboard
* Facility intelligence
* Medicine monitoring
* Geographic risk visualisation
* Demand-surge simulation
* Resource-prioritisation insights

### Phase 2 — Predictive Intelligence

* Predictive machine-learning models
* Demand forecasting
* Medicine stock-out forecasting
* Facility capacity forecasting
* Advanced anomaly detection

### Phase 3 — Real-Time Intelligence

* Real-time healthcare data integration
* Live facility status
* Real-time medicine inventory
* Automated alerts
* Supply-chain monitoring

### Phase 4 — Network-Level Coordination

* Multi-facility resource optimisation
* Advanced crisis simulation
* Cross-facility resource redistribution
* Supplier disruption modelling
* Scenario-based emergency planning

---

# 🌍 Potential Impact

CareMesh is designed to support:

* Earlier identification of vulnerable facilities
* Better visibility across healthcare networks
* Proactive medicine and resource planning
* Scenario-based preparedness
* Prioritisation of limited resources
* More informed operational decision-making

These are **intended capabilities and potential benefits**; the current prototype has not been deployed or validated in real healthcare systems.

---

# 🎯 Hackathon Prototype

**Project:** CareMesh
**Category:** Healthcare / AI / Resilience / Decision Support
**Prototype:** Interactive Streamlit application
**Data:** Synthetic healthcare-network data

### Core concept

> **Monitor → Understand → Simulate → Prioritise → Act**

CareMesh aims to help healthcare networks prepare for pressure **before pressure becomes crisis**.

---

# ⚠️ Prototype Disclaimer

CareMesh is currently a **hackathon prototype** developed for demonstrating a healthcare resilience and decision-support concept.

It:

* Uses synthetic data
* Is not a clinical diagnostic system
* Does not provide medical advice
* Has not been validated for clinical use
* Does not replace healthcare professionals or emergency decision-makers

Any future real-world deployment would require appropriate validation, security, privacy protections, regulatory compliance, and integration with authorised healthcare data systems.

---

# 👥 Team

**Team / Developer:** Anuja Deore

Built for **Code for Communities 2 — Hack2Skill**

---

## 📌 Project Vision

### **CareMesh**

### *From reactive healthcare response to proactive resilience intelligence.*

```text
MONITOR
   ↓
IDENTIFY
   ↓
SIMULATE
   ↓
PRIORITISE
   ↓
RESPOND
```

---
