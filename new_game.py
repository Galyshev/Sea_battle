from fastapi import APIRouter, Request, Body
from starlette.templating import Jinja2Templates
from fastapi import Depends
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from alchemy import get_async_session #ДЛЯ ЗАПУСКА ЧЕРЕЗ КОНСОЛЬ
from BD.model_bd import player_game_field, comp_game_field   #ДЛЯ ЗАПУСКА ЧЕРЕЗ КОНСОЛЬ
# from alchemy import get_async_session       #ДЛЯ ЗАПУСКА ЧЕРЕЗ ДОКЕР
# from ИВ.model_bd import player_game_field, comp_game_field      #ДЛЯ ЗАПУСКА ЧЕРЕЗ ДОКЕР

router = APIRouter(
    prefix='/new',
    tags=['New_game']
)

templates = Jinja2Templates(directory="templates")

@router.post('/')
async def start_new(request: Request, session: AsyncSession = Depends(get_async_session)):
    # ГЕНЕРАЦИЯ ИГРОВЫХ ПОЛЕЙ для текущей игры
    current_datetime = str(datetime.today())
    vertical_index = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    horizontal_index = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for v in vertical_index:
        for h in horizontal_index:
            stmt_p = insert(player_game_field).values(vert_index=v, horiz_index=h, ship="0", id_ship="0",
                                                    create_date=current_datetime, field_class='play_btn_free')
            await session.execute(stmt_p)

            stmt_c = insert(comp_game_field).values(vert_index=v, horiz_index=h, ship="0", id_ship="0",
                                                  create_date=current_datetime, field_class='play_btn_free')
            await session.execute(stmt_c)
            await session.commit()

    query_p = select(player_game_field).where(player_game_field.c.create_date == current_datetime)
    result = await session.execute(query_p)
    rez_pl = result.all()

    query_c = select(comp_game_field).where(comp_game_field.c.create_date == current_datetime)
    result = await session.execute(query_c)
    rez_comp = result.all()

    return templates.TemplateResponse('new_game.html', {"request": request, "rez_pl": rez_pl, "rez_comp": rez_comp,
                                                        "v_index": vertical_index})

@router.post('/generate')
async def generate(request: Request, data:str =Body()):
    rez = data.split('=')[1]
    print(rez)
    play_btn_class = "play_btn_red"

    return templates.TemplateResponse('new_game.html', {"request": request, "play_btn_class": play_btn_class})