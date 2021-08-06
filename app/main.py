from fastapi import FastAPI
from .routes import users


app = FastAPI()

app.include_router(users.router)

@app.get('/')
async def root():
    return {'message': 'REST Back-end Challenge 20201209 Running'}