from dataclasses import dataclass

from sqlwhisper.db_lib import FUTURES_TABLE

@dataclass
class TextSqlPair:
    text: str
    sql_str: str

stock_text_sql_pairs = [
    TextSqlPair(
        'Give me the latest price for GC=F',
        (
        "SELECT * "
        f"FROM {FUTURES_TABLE} "
        "WHERE symbol = 'GC=F' "
        "ORDER BY trade_date D ESC"
        "LIMIT 1"
        )
    ),
    TextSqlPair(
        'Give me the latest price for gold',
        (
        "SELECT * "
        f"FROM {FUTURES_TABLE} "
        "WHERE symbol = 'GC=F' "
        "ORDER BY trade_date DESC "
        "LIMIT 1"
        )
    )
]

