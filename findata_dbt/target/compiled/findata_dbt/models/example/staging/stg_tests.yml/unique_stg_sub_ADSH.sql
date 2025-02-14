
    
    

select
    ADSH as unique_field,
    count(*) as n_records

from FIN_DATA.DEV.stg_sub
where ADSH is not null
group by ADSH
having count(*) > 1


