
  create or replace   view FIN_DATA.DEV.stg_pre
  
   as (
    with pre as (
    select
        ADSH,
        REPORT,
        LINE,
        TAG,
        PLABEL
    from FIN_DATA.DEV.raw_pre
)
select * from pre
  );

