with transformed as (
    select 
        n.ADSH,
        n.TAG,
        n.VERSION,
        n.VALUE,
        n.coreg,
        n.footnote,
        s.CIK,
        s.NAME as company_name
    from FIN_DATA.DEV.stg_num n
    left join FIN_DATA.DEV.stg_sub s 
    on n.ADSH = s.ADSH
)
select * from transformed