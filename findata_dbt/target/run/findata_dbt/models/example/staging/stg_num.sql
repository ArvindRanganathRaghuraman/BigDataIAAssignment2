
  create or replace   view FIN_DATA.DEV.stg_num
  
   as (
    with num as (
    select
        ADSH,
        TAG,
        VERSION,
        VALUE,
        coreg,
        footnote
    from FIN_DATA.DEV.raw_num
)
select * from num
  );

