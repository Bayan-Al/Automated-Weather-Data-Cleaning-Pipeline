# Automated Weather Data Cleaning Pipeline

An automated, defensive data engineering pipeline that ingests disparate corporate data silos (CSV, JSON, and Excel), executes comprehensive architectural diagnostics, and relationally joins them into an enterprise Final Dataset optimized for business intelligence.

## 🏢 Corporate Data Silos Ingested
*   `temperature.csv`: Historical core temperatures.
*   `environmental.json`: Atmospheric metrics (Humidity, Wind Speed).
*   `summary.xlsx`: Categorical business summaries and precipitation tracking.

## 🛠️ Data Quality Framework (The 6 Core Dimensions)
Rather than executing blind merges, this pipeline acts as an automated Data Quality Governance system, mapping code architecture directly to global data management standards:

1. **Completeness:** Evaluates null profiles using `.isnull().sum()` and automatically imputes missing categorical data (`Precip Type`) with governed default states.
2. **Uniqueness:** Detects duplicate timestamps using `.duplicated()` and programmatically eliminates them to prevent downstream row-inflation.
3. **Integrity (Conformity):** Audits heterogeneous string date schemas across formats and coerces them into a single, unified `datetime64[ns, UTC]` timeline.
4. **Consistency:** Aligns disparate corporate data keys perfectly across different storage layers before executing relational inner joins.
5. **Accuracy:** Deploys a mathematical `Statistical Range Check` using descriptive metrics to identify and flag physically impossible atmospheric anomalies.
6. **Timeliness:** Structured as a modular, production-ready automation script capable of processing fresh transactional drop-zone data instantly.

## 📁 Repository Structure

```text
automated-weather-pipeline/
│
├── 📁 raw_data/
│   ├── source_temperature.csv
│   ├── source_environmental.json
│   └── source_summary.xlsx
│
├── 📁 final_output/
│   └── final_dataset.csv
│
├── README.md
└── automated_weather_pipeline.py
