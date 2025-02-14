
  create or replace   view FIN_DATA.DEV.fact_financials
  
   as (
    with financials as (
    select 
        n.ADSH,
        n.TAG,
        sum(n.VALUE) as total_value,
        s.CIK,
        s.NAME as company_name
    from FIN_DATA.DEV.int_num n
    left join FIN_DATA.DEV.stg_sub s 
    on n.ADSH = s.ADSH
    group by n.ADSH, n.TAG, s.CIK, s.NAME
)
select * from financials
  );

