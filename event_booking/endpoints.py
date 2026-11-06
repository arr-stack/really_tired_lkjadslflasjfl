
from datetime import time, datetime
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from authx import AuthXConfig, AuthX
from EventORM import Session, User, Events, Registarations
from sqlalchemy import insert, select, update
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory='templates')

config = AuthXConfig()
config.JWT_SECRET_KEY = '_renmerry_'
config.JWT_ACCESS_COOKIE_NAME = 'access_token'
config.JWT_TOKEN_LOCATION = ['cookies']
secret = AuthX(config=config)

def timeslots_gen(time_start: time, time_end: time):
    slots = []
    current_minutes = time_start.hour * 60 + time_start.minute
    end_minutes = time_end.hour * 60 + time_end.minute
    step_minutes = 120

    while current_minutes + step_minutes <= end_minutes:
        start_slot = time(current_minutes // 60, current_minutes % 60)
        end_slot = time((current_minutes + step_minutes) // 60, (current_minutes + step_minutes) % 60)

        slots.append((start_slot, end_slot))
        current_minutes += step_minutes

    return slots



@app.get('/home')
def home(request: Request):
    with Session() as session:
        events = session.scalars(select(Events)).all()
        slots_events = []

        for event in events:
            slots = timeslots_gen(event.start_time, event.end_time)

            formatted = [
                {"start": s[0].strftime("%H:%M"), "end": s[1].strftime("%H:%M")}
                for s in slots
            ]
            slots_events.append({
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "people_amount": event.people_amount,
                "people_max": event.people_max,
                "slots": formatted
            })
    return templates.TemplateResponse(request, 'index.html', {'events': slots_events})

@app.post('/home', dependencies=[Depends(secret.access_token_required)])
def get(user_id: int = Form(), event_id: int = Form(), time_slot: str = Form()):
    start_str, end_str = time_slot.split('-')
    slot_start = datetime.strptime(start_str, "%H:%M").time()
    slot_end = datetime.strptime(end_str, "%H:%M").time()
    with Session() as session:
        event = session.execute(insert(Registarations).values(event_id=event_id, user_id=user_id))

        if event.people_amount == event.people_max:
            raise HTTPException(status_code=400, detail='No more people')
        session.execute(
            insert(Registarations).values(event_id=event.id, user_id=user_id,
                                          time_slot_start=slot_start, time_slot_end=slot_end)
        )
        session.execute(update(Events).where(Events.id == event.id).values(people_amount=event.people_amount + 1))
        session.commit()

    return RedirectResponse(url='/home', status_code = status.HTTP_303_SEE_OTHER)


@app.get("/login/sign_in")
def sign_in(request: Request):
    return templates.TemplateResponse(request, 'sign_in.html')

@app.get("/login/sign_up")
def sign_up(request: Request):
    return templates.TemplateResponse(request, 'sign_up.html')

@app.post("/login/sign_in")
def log_in(email: str = Form(), password: str = Form()):
    with Session() as session:
        result = select(User).where(User.email == email)
        data = session.scalars(result).first()
        if data and data.password == password:
            token = secret.create_access_token(uid=str(data.id))
            response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return response
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post('login/sign_up')
def sign_up(username: str = Form(), email: str = Form(), password: str = Form()):
    with Session() as session:
        session.execute(insert(User).values(username=username, email=email, password=password))
        session.commit()
        return RedirectResponse(url='/home', status_code= status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)