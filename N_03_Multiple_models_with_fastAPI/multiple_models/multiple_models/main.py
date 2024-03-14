from typing import Optional, List
from multiple_models import settings
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True): #only Hero is with table = True - means class Hero represents table in the database. It is both the pydantic model (help to automatically validate and filter) and SQLAlchemy model (it will create a table)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

class HeroCreate(SQLModel): #only pydantic model- won't be used with the database,but only to declare data schemas for the API 
    name: str #share some common fields
    secret_name: str #share some common fields
    age: Optional[int] = None #share some common fields

class HeroRead(SQLModel): #only pydantic model - won't be used with the database,but only to declare data schemas for the API 
    id: int
    name: str #share some common fields
    secret_name: str #share some common fields
    age: Optional[int] = None #share some common fields

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
@app.post("/heroes/", response_model=HeroRead) # HeroRead will validate that all the data that we promised is there and will remove any data we didn't declare.
def create_hero(hero: HeroCreate): 
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero) #model_validate function checks the list to ensure everything is correct and fits the expected format and rules for a hero
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero   
    
#now we insert hero we want to read it 
@app.get("/heroes/", response_model=List[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes