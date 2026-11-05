from pydantic import BaseModel, Field

class ResisterEval(BaseModel):
    id: int = Field()
    user_id: int = Field()
    event_id: int = Field()

class EventsEval(BaseModel):
    id: int = Field()
    title: str = Field(min_length=1)
    date: str = Field()
    description: str = Field(min_length=1)
    people_amount: int = Field(ge=0)
    people_max: int = Field(ge=0)


class UserLogin(BaseModel):
    id: int = Field()
    email: str = Field()
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)
