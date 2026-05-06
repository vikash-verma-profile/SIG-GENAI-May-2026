
  
    

create or replace transient table TESTDB.PUBLIC.mart_revenue_by_customer_2025
    
    
    
    as ({
    'models': [
        {
            'name': 'revenue_by_customer',
            'reference_model': 'stg_customers',
            'source_model': 'customers',
            'source_table': 'stg_customers',
            'target_table': 'Revenue for an order',
            'fields': ['customer_id', 'customer_name']
        },
        {
            'name': 'top_customers_by_revenue_2025',
            'reference_model': 'stg_customers',
            'source_model': 'customers',
            'source_table': 'stg_customers',
            'target_table': 'Revenue for an order by customer',
            'fields': ['customer_id', 'customer_name', 'revenue']
        }
    ]
}
    )
;


  