from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select, Field     
from typing import Optional, Annotated


db_url = "postgresql://neondb_owner:yj8bQvLhu1Gd@ep-winter-mountain-a18bp9co.ap-southeast-1.aws.neon.tech/empty?sslmode=require"
engine = create_engine(db_url)

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

class Hero(HeroBase, table=True):
    id: int = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass    

class HeroResponse(HeroBase):
    id: int
    



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_db():
    with Session(engine) as session:
        yield session

@app.get("/heroes")
def get_heroes(session: Annotated[Session, Depends(get_db)]):
    heroes = session.exec(select(Hero)).all()
    return heroes

@app.post("/heroes", response_model=HeroResponse)
def create_hero(hero: HeroCreate , db: Annotated[Session, Depends(get_db)]):
    print("Data from Client: ", hero)
    hero_to_insert = Hero.model_validate(hero)
    print("Data after model validate: ", hero_to_insert)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert
