from sqlalchemy import Table, Column, Integer, String, MetaData


metadata = MetaData()

player_game_field = Table(
    "player_game_field",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("vert_index", String),
    Column("horiz_index", String),
    Column("ship", String),
    Column("id_ship", String),
    Column("create_date", String),
    Column("field_class", String),

)
comp_game_field = Table(
    "comp_game_field",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("vert_index", String),
    Column("horiz_index", String),
    Column("ship", String),
    Column("id_ship", String),
    Column("create_date", String),
    Column("field_class", String),

)