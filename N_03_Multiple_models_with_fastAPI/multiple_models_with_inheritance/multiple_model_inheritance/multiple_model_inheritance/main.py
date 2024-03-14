from typing import Optional, List
from multiple_model_inheritance import settings
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select



class HeroBase(SQLModel): #no table attribute here
    name: str = Field(index=True) #this is not a table model still we can write Field(index=True) - Hero will use it after inheritance  
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class Hero(HeroBase, table=True): #now it doesnot inherit from SQLModel but from HeroBase
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroCreate(HeroBase): 
    pass #The fields we need to create are exactly the same as the ones in the HeroBase model. So we don't have to add anything.

class HeroRead(HeroBase):
    id: int

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