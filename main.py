from fastapi import FastAPI
from api import player, auth, national, club

app = FastAPI()

# Init database
@app.on_event("startup")
async def startup():
    '''
    from db import Base, engine
    # from db import db_init
    from models.player import Player
    from models.club import Club
    from models.national import National
    from models.user import User
    Base.metadata.create_all(bind=engine)
    # db_init(engine)
    '''

    from mongo import get_mongo_client
    app.state.mongo_client = get_mongo_client()
    app.state.mongo_db = app.state.mongo_client["pokazna"]


# Register routes
app.include_router(player.router)
app.include_router(auth.router)
app.include_router(national.router)
app.include_router(club.router)
