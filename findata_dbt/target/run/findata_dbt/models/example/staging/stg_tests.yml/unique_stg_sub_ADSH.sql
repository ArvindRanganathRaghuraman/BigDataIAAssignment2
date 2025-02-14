select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    ADSH as unique_field,
    count(*) as n_records

from FIN_DATA.DEV.stg_sub
where ADSH is not null
group by ADSH
having count(*) > 1



      
    ) dbt_internal_test