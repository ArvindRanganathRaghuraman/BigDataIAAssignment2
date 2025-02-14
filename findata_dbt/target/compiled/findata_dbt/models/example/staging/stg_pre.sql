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