# 📦 dbt Project 

```
snowflake-dbt-semantic-demo
```

---

# 📂 Full Project Structure

```
snowflake-dbt-semantic-demo/
│
├── README.md
├── .gitignore
├── dbt_project.yml
├── packages.yml
│
├── models/
│   ├── sources.yml
│   ├── staging/
│   │   ├── stg_stripe_payments.sql
│   │   └── stg_customers.sql
│   │
│   ├── marts/
│   │   ├── core/
│   │   │   ├── dim_customers.sql
│   │   │   ├── fct_payments.sql
│   │   │   └── schema.yml
│   │   │
│   │   └── semantic/
│   │       └── revenue_semantic.yml
│   │
│   └── snapshots/
│       └── customers_snapshot.sql
│
└── macros/
```

---

# 1️⃣ README.md

````markdown
# Snowflake + dbt Semantic Revenue Model Demo

This project demonstrates a production-style analytics engineering workflow using:

- Snowflake (Cloud Data Warehouse)
- dbt (Data Build Tool)
- Star Schema Modeling
- dbt Tests
- dbt Semantic Layer
- Snapshots (SCD Type 2)
- Incremental Models

---

## Architecture

RAW (Snowflake)
    ↓
Staging Layer (Cleaning + Renaming)
    ↓
Core Mart Layer (Star Schema)
    ↓
Semantic Layer (Metrics + Entities)
    ↓
BI / Metric API

---

## Business Problem

How much revenue are we generating monthly, and how is it trending over time?

---

## Setup

1. Configure `profiles.yml` for Snowflake
2. Install dependencies

```bash
dbt deps
dbt run
dbt test
dbt docs generate
dbt docs serve
````

---

## Models Included

* `stg_stripe_payments`
* `stg_customers`
* `dim_customers`
* `fct_payments`
* Semantic model for revenue
* Snapshot example (SCD Type 2)

---

## Skills Demonstrated

* Warehouse-native ELT
* Star schema modeling
* Incremental modeling
* Referential integrity testing
* Semantic layer metric abstraction
* Slowly changing dimensions
* Production project structure

```

---

# 2️⃣ .gitignore

```

target/
dbt_packages/
logs/
.env

````

---

# 3️⃣ dbt_project.yml

```yaml
name: 'snowflake_dbt_semantic_demo'
version: '1.0'
config-version: 2

profile: 'snowflake_profile'

model-paths: ["models"]
snapshot-paths: ["models/snapshots"]
macro-paths: ["macros"]

models:
  snowflake_dbt_semantic_demo:
    staging:
      materialized: view
    marts:
      core:
        materialized: table
      semantic:
        materialized: view
````

---

# 4️⃣ packages.yml

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```

Run:

```
dbt deps
```

---

# 5️⃣ models/sources.yml

```yaml
version: 2

sources:
  - name: raw
    database: RAW
    schema: PUBLIC

    tables:
      - name: stripe_payments
      - name: customers
```

---

# 6️⃣ STAGING MODELS

---

## models/staging/stg_stripe_payments.sql

```sql
{{ config(materialized='view') }}

select
    id as payment_id,
    customer_id,
    amount / 100.0 as amount_usd,
    currency,
    created_at::timestamp as payment_timestamp,
    date(created_at) as payment_date
from {{ source('raw', 'stripe_payments') }}
```

---

## models/staging/stg_customers.sql

```sql
{{ config(materialized='view') }}

select
    id as customer_id,
    email,
    created_at::timestamp as customer_created_at
from {{ source('raw', 'customers') }}
```

---

# 7️⃣ CORE MART MODELS

---

## models/marts/core/dim_customers.sql

```sql
{{ config(materialized='table') }}

select
    customer_id,
    email,
    customer_created_at
from {{ ref('stg_customers') }}
```

---

## models/marts/core/fct_payments.sql

```sql
{{ config(
    materialized='incremental',
    unique_key='payment_id'
) }}

select
    p.payment_id,
    p.customer_id,
    p.payment_date,
    p.payment_timestamp,
    p.amount_usd
from {{ ref('stg_stripe_payments') }} p

{% if is_incremental() %}
where p.payment_timestamp > (select max(payment_timestamp) from {{ this }})
{% endif %}
```

This shows incremental production modeling capability.

---

# 8️⃣ TESTS + DOCUMENTATION

## models/marts/core/schema.yml

```yaml
version: 2

models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique

  - name: fct_payments
    description: "Fact table containing payment transactions"
    columns:
      - name: payment_id
        tests:
          - not_null
          - unique

      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

---

# 9️⃣ SNAPSHOT (SCD Type 2)

## models/snapshots/customers_snapshot.sql

```sql
{% snapshot customers_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='customer_created_at'
    )
}}

select *
from {{ ref('stg_customers') }}

{% endsnapshot %}
```

Run:

```
dbt snapshot
```

This demonstrates handling dimensional history.

---

# 🔟 SEMANTIC LAYER

## models/marts/semantic/revenue_semantic.yml

```yaml
semantic_models:
  - name: payments
    model: ref('fct_payments')
    description: "Fact table for Stripe payments"

    entities:
      - name: payment
        type: primary
        expr: payment_id

      - name: customer
        type: foreign
        expr: customer_id

    dimensions:
      - name: payment_date
        type: time
        expr: payment_date
        type_params:
          time_granularity: day

    measures:
      - name: total_revenue
        agg: sum
        expr: amount_usd

      - name: total_payments
        agg: count
        expr: payment_id

metrics:
  - name: monthly_revenue
    label: "Monthly Revenue"
    type: simple
    type_params:
      measure: total_revenue
    time_grains: [month]
```

---

# 🧠 Optional: Snowflake DDL (For Demo Data)

If you want to include a `/demo_data.sql` file:

```sql
create or replace table RAW.PUBLIC.customers (
  id string,
  email string,
  created_at timestamp
);

create or replace table RAW.PUBLIC.stripe_payments (
  id string,
  customer_id string,
  amount number,
  currency string,
  created_at timestamp
);
```

---

# 🚀 What This Repository Demonstrates

* Warehouse-first ELT
* Incremental models
* Referential integrity enforcement
* Snapshotting for SCD
* Semantic modeling
* Metric abstraction
* Production folder architecture
* Reusable package integration
* Snowflake-native transformations



