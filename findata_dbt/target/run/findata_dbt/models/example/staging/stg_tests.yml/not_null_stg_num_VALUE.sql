select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select VALUE
from FIN_DATA.DEV.stg_num
where VALUE is null



      
    ) dbt_internal_test