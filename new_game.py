from fastapi import APIRouter, Request, Body
from starlette.templating import Jinja2Templates
from fastapi import Depends
from sqlalchemy import select, update, insert, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


from alchemy import get_async_session #ДЛЯ ЗАПУСКА ЧЕРЕЗ КОНСОЛЬ
from BD.model_bd import player_game_field, comp_game_field, ships_flag, ships_koord   #ДЛЯ ЗАПУСКА ЧЕРЕЗ КОНСОЛЬ
# from alchemy import get_async_session       #ДЛЯ ЗАПУСКА ЧЕРЕЗ ДОКЕР
# from ИВ.model_bd import player_game_field, comp_game_field      #ДЛЯ ЗАПУСКА ЧЕРЕЗ ДОКЕР

router = APIRouter(
    prefix='/new',
    tags=['New_game']
)

templates = Jinja2Templates(directory="templates")
# Глобальные переменные
vertical_index = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
horizontal_index = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
ships = ["sh_4", "sh_3_1", "sh_3_2", "sh_2_1", "sh_2_2", "sh_2_3", "sh_1_1", "sh_1_2", "sh_1_3", "sh_1_4"]
async def get_game_id(session: AsyncSession = Depends(get_async_session)):
    query = select(player_game_field.c.id).order_by(desc(player_game_field.c.id))
    result = await session.execute(query)
    last_id = result.all()[0][0]

    query = select(player_game_field.c.create_date).where(player_game_field.c.id == last_id)
    result = await session.execute(query)
    ID_GAME = result.all()[0][0]
    return ID_GAME


@router.post('/')
async def start_new(request: Request, session: AsyncSession = Depends(get_async_session)):
    # ГЕНЕРАЦИЯ ИГРОВЫХ ПОЛЕЙ для текущей игры
    current_datetime = str(datetime.today())
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

    # Сброс размещенных кораблей в старой игре, иначе будут некативны
    query = delete(ships_flag)
    await session.execute(query)
    await session.commit()
    for sh in ships:
        ship_rang = sh.split('_')[1]
        ship_class = sh[0:4]
        stmt = insert(ships_flag).values(id_ship=sh, flag='activ', ship_class=ship_class, ship_rang=ship_rang)
        await session.execute(stmt)
        await session.commit()
    query_sh = select(ships_flag)
    result = await session.execute(query_sh)
    rez_ship = result.all()

    return templates.TemplateResponse('new_game.html', {"request": request, "rez_pl": rez_pl, "rez_comp": rez_comp,
                                                        "v_index": vertical_index, "rez_ship": rez_ship})

@router.post('/placement_of_ships')
async def placement_of_ships(request: Request, data:str =Body(), session: AsyncSession = Depends(get_async_session)):
    # Обновление игрового поля
    id_ship=''
    id_game = await get_game_id(session)
    query_p = select(player_game_field).where(player_game_field.c.create_date == id_game)
    result = await session.execute(query_p)
    rez_pl = result.all()
    query_sh = select(ships_flag)
    result = await session.execute(query_sh)
    rez_ship = result.all()

    clic = data.split('=')[1]

    if clic == 'sh_3_1' or clic == 'sh_3_2':
        id_ship = clic
        sh_class = clic[0:4]
        ship_rang = clic.split('_')[1]
        id_game = await get_game_id(session)
        query_p = select(player_game_field).where(player_game_field.c.create_date == id_game)
        result = await session.execute(query_p)
        rez_pl = result.all()
        status = 'new'

        return templates.TemplateResponse('place.html', {"request": request, "rez_pl": rez_pl,
                                                            "v_index": vertical_index, "id": id_ship, "sh_class": sh_class,
                                                         "ship_rang": ship_rang, 'status': status})

    return templates.TemplateResponse('new_game.html', {"request": request, "rez_pl": rez_pl,
                                                        "v_index": vertical_index, "rez_ship": rez_ship, "selected": id_ship})

@router.post('/placement_detail')
async def placement_of_ships(request: Request, data:str =Body(), session: AsyncSession = Depends(get_async_session)):
    # Обновление игрового поля

    id_game = await get_game_id(session)
    query_p = select(player_game_field).where(player_game_field.c.create_date == id_game)
    result = await session.execute(query_p)
    rez_pl = result.all()

    clic = data.split('=')[1]
    koor = clic.split('+')[0]
    x_koor = koor.split('-')[1]
    y_koor = koor.split('-')[0]
    id = clic.split('+')[-1]
    rang = id.split('_')[1]
    sh_class = id[0:4]

    # проверка координаты на то, что поле уже занято
    error = ''
    query_p = select(player_game_field).where(player_game_field.c.vert_index == y_koor,
                                              player_game_field.c.horiz_index == x_koor,
                                              player_game_field.c.create_date == id_game
                                              )
    result = await session.execute(query_p)
    rez_chk = result.all()
    for chk in rez_chk:
        if chk.ship != '0':
            error = 'Клетка уже занята'
            return templates.TemplateResponse('place.html', {"request": request, "rez_pl": rez_pl,
                                                             "v_index": vertical_index, "id": id, "sh_class": sh_class,
                                                             "ship_rang": rang, 'error': error})
        else:
            # для трехпалубных
            if rang == '3':
                query = select(ships_koord).where(ships_koord.c.id_ship == id)
                result = await session.execute(query)
                rez_chk_koor = result.all()
                # если корбаля нет в базе - заводятся координаты первой клетки
                if len(rez_chk_koor) == 0:
                    stmt = insert(ships_koord).values(id_ship=id, a_x=x_koor, a_y=y_koor, status='work')
                    await session.execute(stmt)
                    await session.commit()

                elif len(rez_chk_koor) != 0:
                    for chk_koor in rez_chk_koor:
                        # если нет координат второй клетки - заносятся в базу
                        if chk_koor.b_x == None:
                            stmt = update(ships_koord).values(id_ship=id, b_x=x_koor, b_y=y_koor, status='work')
                            await session.execute(stmt)
                            await session.commit()

                        # # если нет координат третьей клетки - заносятся в базу
                        elif chk_koor.c_x == None:
                            stmt = update(ships_koord).values(id_ship=id, c_x=x_koor, c_y=y_koor, status='work')
                            await session.execute(stmt)
                            await session.commit()

                        # если все три координаты существуют, но есть еще одно нажатие на поле размещения -
                        # сообщение об ошибке, обнуление базы по айди корабля и размещение заново
                        else:
                            error = 'Ошибка с размещением корабля (количество клеток). Попробуйте еще раз'
                            query = delete(ships_koord).where(ships_koord.c.id_ship == id)
                            await session.execute(query)
                            await session.commit()
                            status = 'new'
                            return templates.TemplateResponse('place.html', {"request": request, "rez_pl": rez_pl,
                                                                      "v_index": vertical_index, "id": id,
                                                                      "sh_class": sh_class,
                                                                      'status': status,
                                                                      "ship_rang": rang, 'error': error})

                query = select(ships_koord).where(ships_koord.c.id_ship == id)
                result = await session.execute(query)
                rez_chk_koor = result.all()
                return templates.TemplateResponse('place.html', {"request": request, "rez_pl": rez_pl,
                                                                 "v_index": vertical_index, "id": id,
                                                                 "sh_class": sh_class,
                                                                 'rez_chk_koor': rez_chk_koor,
                                                                 "ship_rang": rang, 'error': error})

    return templates.TemplateResponse('place.html', {"request": request, "rez_pl": rez_pl,
                                                     "v_index": vertical_index, "id": id, "sh_class": sh_class,
                                                     "ship_rang": rang, 'error': error})
