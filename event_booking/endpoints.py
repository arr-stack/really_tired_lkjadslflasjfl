from http.client import responses

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from authx import AuthXConfig, AuthX
from EventORM import Session, User, Events
from sqlalchemy import insert, select, update
from evaluation import UserLogin, ResisterEval, EventsEval
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory='templates')

config = AuthXConfig()
config.JWT_SECRET_KEY = '_renmerry_'
config.JWT_ACCESS_COOKIE_NAME = 'access_token'
config.JWT_TOKEN_LOCATION = ['cookies']
secret = AuthX(config=config)

@app.get('/home')
def home(request: Request, success: bool | None):
    return templates.TemplateResponse(request, 'index.html', {'success': success})

@app.post('/home', dependencies=[Depends(secret.access_token_required)])
def get(user_id: int = Form(), event_id: int = Form()):
    # with Session() as session:
    #     session.execute(insert(ResisterEval).values(event_id=event_id, user_id=user_id))
    #     people_amount = session.execute(select(Events.people_amount).where(Events.id == event_id))
    #     people_amount += 1
    #     session.execute(update(Events).where(Events.id == event_id).values(people_amount=people_amount))
    #     session.commit()
    print(user_id)
    print(event_id)
    people_amount = 0
    people_amount += 1
    return RedirectResponse(url='/home', status_code = status.HTTP_303_SEE_OTHER)


@app.get('/home', )
def home_reg(request: Request):
    return templates.TemplateResponse(request, 'index.html')


"""RESITSRATION PROCESS"""
@app.post("/login/sign_in")
def log_in(user_: UserLogin):
    with Session() as session:
        result = select(User).where(User.username == user_.username)
        data = session.scalars(result).first()
        if data and data.password == user_.password:
            token = secret.create_access_token(uid=str(data.id))
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return response
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post('login/sign_up')
def sign_up(username: str, email: str, password: str):
    with Session() as session:
        session.execute(insert(User).values(username=username, email=email, password=password))
        session.commit()
        return RedirectResponse(url='/home', status_code= status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)