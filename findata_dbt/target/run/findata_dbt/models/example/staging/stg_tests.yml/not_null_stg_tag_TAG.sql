select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select TAG
from FIN_DATA.DEV.stg_tag
where TAG is null



      
    ) dbt_internal_test