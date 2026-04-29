# Queens Supermarket Sales Analytics Pipeline
[![Live Demo](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://supermarket-etl-pipeline-asqyvpcrxuxfnxg35byc4c.streamlit.app/)


End-to-End ETL Pipeline and Star-Schema Data Warehouse for Queens Supermarket Sales Analytics

---

## Description

This project simulates a real-world data engineering solution for Midroc Commerce, specifically for their Queens Supermarket chain (in partnership with Carrefour). 

It covers the complete data lifecycle — from raw data ingestion to transformation, dimensional modeling in a MySQL data warehouse, data quality validation, and an interactive business intelligence dashboard. The pipeline is designed to support reporting, demand forecasting, inventory optimization, and executive decision-making.

---

## Problem Statement

Midroc Commerce manages high-volume daily sales transactions across multiple Queens Supermarket branches. However, data is scattered across ERP and POS systems, leading to:

- Poor visibility into sales performance and branch contribution
- Inconsistent and delayed reporting
- Difficulty in tracking product performance and customer behavior
- Challenges in inventory management and demand forecasting
- Lack of centralized, analytics-ready data for business teams

---

## Solution

Designed and implemented a complete ETL/ELT pipeline using Medallion Architecture (Bronze → Silver → Gold) and a Star Schema Data Warehouse in MySQL.

### Key Components Delivered:

- **Synthetic Data Generation**: Realistic supermarket sales dataset mimicking Ethiopian retail operations
- **ETL Pipeline**: Modular extraction, cleaning, transformation, and loading using Python and PySpark-ready logic
- **Star Schema Modeling**: Properly designed dimension and fact tables with surrogate keys and relationships
- **Data Quality Framework**: Comprehensive validation, completeness, validity, and uniqueness checks
- **Interactive Dashboard**: Business-friendly Streamlit dashboard for self-service analytics
- **Documentation & Governance**: Full data lineage, quality reports, and metadata

---

## Business Recommendation

Implementing this data warehouse and analytics solution enables Midroc Commerce to:

- Identify top-performing branches and underperforming product lines
- Optimize inventory levels and reduce stockouts/overstock
- Improve demand forecasting accuracy using historical trends
- Understand customer payment preferences (especially Mobile Money vs Card)
- Support data-driven decisions for expansion and promotional strategies

**Recommended Next Steps**: Migrate to a cloud data warehouse (AWS Redshift / Google BigQuery), implement real-time ingestion using Kafka, and integrate with Midroc’s central ERP system.

---

## Tech Stack Used

| Category              | Technologies                                      |
|-----------------------|---------------------------------------------------|
| **Language**          | Python 3                                          |
| **Data Processing**   | Pandas, PySpark (ready)                           |
| **Database**          | MySQL (Star Schema)                               |
| **ORM & Connectivity**| SQLAlchemy, PyMySQL                               |
| **Visualization**     | Streamlit, Plotly                                 |
| **Data Quality**      | Custom DQ Framework + Validation Rules            |
| **Environment**       | dotenv, Jupyter Notebook                          |
| **Architecture**      | Medallion (Bronze → Silver → Gold), Star Schema   |
| **Version Control**   | Git                                               |

---
