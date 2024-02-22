from fastapi import APIRouter, Request, Body
from starlette.templating import Jinja2Templates


router = APIRouter(
    prefix='/new',
    tags=['New_game']
)

templates = Jinja2Templates(directory="templates")

@router.post('/')
async def start_new(request: Request):
    play_btn_class = "play_btn_free"
    return templates.TemplateResponse('new_game.html', {"request": request, "play_btn_class": play_btn_class})

@router.post('/generate')
async def generate(request: Request, data:str =Body()):
    rez = data.split('=')[1]
    print(rez)
    play_btn_class = "play_btn_red"

    return templates.TemplateResponse('new_game.html', {"request": request, "play_btn_class": play_btn_class})