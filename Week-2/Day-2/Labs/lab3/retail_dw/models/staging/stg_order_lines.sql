select
    order_line_id,
    order_id,
    product_id,
    quantity::number(18, 4) as quantity,
    line_total::number(18, 2) as line_total
from {{ source("raw_store", "order_lines") }}
