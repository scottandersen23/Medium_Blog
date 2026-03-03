
-- models/marts/fct_daily_sales.sql

select
    order_date,
    sum(order_total) as total_revenue
from {{ ref('stg_orders') }}
group by order_date
