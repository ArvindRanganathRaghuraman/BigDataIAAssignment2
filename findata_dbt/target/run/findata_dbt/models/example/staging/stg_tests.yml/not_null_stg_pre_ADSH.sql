select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select ADSH
from FIN_DATA.DEV.stg_pre
where ADSH is null



      
    ) dbt_internal_test