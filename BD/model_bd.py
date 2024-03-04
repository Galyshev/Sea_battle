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
ships_flag = Table(
    "ships_flag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_ship", String),
    Column("flag", String),
    Column("ship_class", String),
    Column("ship_rang", String),
)
ships_koord = Table(
    "ships_koord",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_ship", String),
    Column("a_x", String),
    Column("b_x", String),
    Column("c_x", String),
    Column("d_x", String),
    Column("a_y", String),
    Column("b_y", String),
    Column("c_y", String),
    Column("d_y", String),
    Column("status", String),
)