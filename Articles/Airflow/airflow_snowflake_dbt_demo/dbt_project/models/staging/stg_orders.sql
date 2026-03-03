
-- models/staging/stg_orders.sql

select
    order_id,
    customer_id,
    cast(order_total as float) as order_total,
    order_date
from {{ source('raw', 'orders') }}
