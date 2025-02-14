select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select CIK
from FIN_DATA.DEV.stg_sub
where CIK is null



      
    ) dbt_internal_test