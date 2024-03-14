from typing import Optional, List
from response_model import settings
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI() #app is an instance of FastAPI class

# create database and tables on startup 
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#now lets insert data into the Hero table:
@app.post("/heroes/", response_model=Hero) #we pass the same Hero SQLModel class because it is also a Pydentic model - helpful for data validation and filteration 
def create_hero(hero: Hero): #here we define the type "Hero" of input data, so API docs knows the type of data client have to send
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero   
    
#now we insert hero we want to read it 
@app.get("/heroes/", response_model=List[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes