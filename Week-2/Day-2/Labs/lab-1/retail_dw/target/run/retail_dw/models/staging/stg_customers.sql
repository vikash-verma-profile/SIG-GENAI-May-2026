
  create or replace   view TESTDB.PUBLIC.stg_customers
  
  
  
  
  as (
    select
    customer_id,
    trim(name) as customer_name,
    region,
    signup_date::date as signup_date
from TESTDB.raw_store.customers
  );

