with sub as (
    select
        ADSH,
        CIK,
        NAME,
        SIC,
        COUNTRYBA,
        STPRBA,
        CITYBA,
        ZIPBA,
        FORM,
        FY,
        FP
    from FIN_DATA.DEV.raw_sub
)
select * from sub