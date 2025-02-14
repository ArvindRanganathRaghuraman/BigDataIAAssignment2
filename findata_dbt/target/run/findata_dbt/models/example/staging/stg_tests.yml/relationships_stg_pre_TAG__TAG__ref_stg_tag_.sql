select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with child as (
    select TAG as from_field
    from FIN_DATA.DEV.stg_pre
    where TAG is not null
),

parent as (
    select TAG as to_field
    from FIN_DATA.DEV.stg_tag
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



      
    ) dbt_internal_test