import sqlalchemy as sa

def to_tsvector_ix(lang, *columns):
    s = " || ' ' || ".join(columns)
    return sa.sql.func.to_tsvector(lang, sa.text(s))