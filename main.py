import uvicorn
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from new_game import router as router_new


app = FastAPI(
    title='Sea Battle'
)

app.mount("/static", StaticFiles(directory="static"), name='static')

templates = Jinja2Templates(directory="templates")
app.include_router(router_new)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.post('/new')
async def start_new(request: Request):
    response = RedirectResponse(url='/new/')
    return response

@app.post('/continue')
async def start_continue(request: Request, btn_continue=Form()):
    # response = RedirectResponse(url='!!!!')
    # return response
    rez = btn_continue
    return templates.TemplateResponse('tmp.html', {"request": request, "rez": rez})


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=False)