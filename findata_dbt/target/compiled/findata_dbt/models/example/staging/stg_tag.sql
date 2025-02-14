with tag as (
    select DISTINCT TAG, DATATYPE, CRDR, Tlabel, DOC
    from FIN_DATA.DEV.raw_tag
)
select * from tag